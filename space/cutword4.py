# -*- coding:utf-8 -*-
# http://spaces.ac.cn/archives/3924/
# 【中文分词系列】 4. 基于双向LSTM的seq2seq字标注

import re
import numpy as np
import pandas as pd

s = open('msr_train.txt').read()
s = s.split('\r\n')


def clean(s): # 整理一下数据，有些不规范的地方
    if u'“/s' not in s:
        return s.replace(u' ”/s', '')
    elif u'”/s' not in s:
        return s.replace(u'“/s ', '')
    elif u'‘/s' not in s:
        return s.replace(u' ’/s', '')
    elif u'’/s' not in s:
        return s.replace(u'‘/s ', '')
    else:
        return s

s = u''.join(map(clean, s))
s = re.split(u'[，。！？、]/[bems]', s)

data = []   # 生成训练样本
label = []


def get_xy(s):
    s = re.findall('(.)/(.)', s)
    if s:
        s = np.array(s)
        return list(s[:,0]), list(s[:,1])

for i in s:
    x = get_xy(i)
    if x:
        data.append(x[0])
        label.append(x[1])

maxlen = 32
d = pd.DataFrame(index=range(len(data)))
d['data'] = data
d['label'] = label
d = d[d['data'].apply(len) <= maxlen]
d.index = range(len(d))
tag = pd.Series({'s':0, 'b':1, 'm':2, 'e':3, 'x':4})


chars = []  # 统计所有字，跟每个字编号
for i in data:
    chars.extend(i)

chars = pd.Series(chars).value_counts()
chars[:] = range(1, len(chars)+1)

# 生成适合模型输入的格式
from keras.utils import np_utils
d['x'] = d['data'].apply(lambda x: np.array(list(chars[x])+[0]*(maxlen-len(x))))
d['y'] = d['label'].apply(lambda x: np.array(map(lambda y:np_utils.to_categorical(y,5), tag[x].reshape((-1,1)))+[np.array([[0,0,0,0,1]])]*(maxlen-len(x))))

# 设计模型
word_size = 128
maxlen = 32
from keras.layers import Dense, Embedding, LSTM, TimeDistributed, Input, Bidirectional
from keras.models import Model

sequence = Input(shape=(maxlen,), dtype='int32')
embedded = Embedding(len(chars)+1, word_size, input_length=maxlen, mask_zero=True)(sequence)
blstm = Bidirectional(LSTM(64, return_sequences=True), merge_mode='sum')(embedded)
output = TimeDistributed(Dense(5, activation='softmax'))(blstm)
model = Model(input=sequence, output=output)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

batch_size = 1024
history = model.fit(np.array(list(d['x'])), np.array(list(d['y'])).reshape((-1,maxlen,5)), batch_size=batch_size, nb_epoch=50)

# 转移概率，单纯用了等概率
zy = {'be':0.5,
      'bm':0.5,
      'eb':0.5,
      'es':0.5,
      'me':0.5,
      'mm':0.5,
      'sb':0.5,
      'ss':0.5
     }

zy = {i:np.log(zy[i]) for i in zy.keys()}


def viterbi(nodes):
    paths = {'b':nodes[0]['b'], 's':nodes[0]['s']}
    for l in range(1,len(nodes)):
        paths_ = paths.copy()
        paths = {}
        for i in nodes[l].keys():
            nows = {}
            for j in paths_.keys():
                if j[-1]+i in zy.keys():
                    nows[j+i]= paths_[j]+nodes[l][i]+zy[j[-1]+i]
            k = np.argmax(nows.values())
            paths[nows.keys()[k]] = nows.values()[k]
    return paths.keys()[np.argmax(paths.values())]


def simple_cut(s):
    if s:
        r = model.predict(np.array([list(chars[list(s)].fillna(0).astype(int))+[0]*(maxlen-len(s))]), verbose=False)[0][:len(s)]
        r = np.log(r)
        nodes = [dict(zip(['s','b','m','e'], i[:4])) for i in r]
        t = viterbi(nodes)
        words = []
        for i in range(len(s)):
            if t[i] in ['s', 'b']:
                words.append(s[i])
            else:
                words[-1] += s[i]
        return words
    else:
        return []

not_cuts = re.compile(u'([\da-zA-Z ]+)|[。，、？！\.\?,!]')


def cut_word(s):
    result = []
    j = 0
    for i in not_cuts.finditer(s):
        result.extend(simple_cut(s[j:i.start()]))
        result.append(s[i.start():i.end()])
        j = i.end()
    result.extend(simple_cut(s[j:]))
    return result


s = """
吉林省长春药店
北京大学生前来应聘，为人民服务，独立自主和平等互利的原则，为人民办公益，他说的确实在理，有意见分歧。
动态规划：这事的确定不下来
“组合型歧义”，这个人的个人恩怨。这扇门的把手，把手抬起来

中外科学名著、提高产品质量、鞭炮声响彻夜空、努力学习语法规则
已结婚的和尚未结婚的青年都要实行计划生育
他是研究生物化学的，也研究生命的起源。他从马上下来

现任主席为何鲁丽，费孝通向人大常委会提交书面报告，邓颖超生前珍藏的书画作品，陈忠和率领的中国女排，成思危来到人民日报社"""
print(' '.join(cut_word(s)))