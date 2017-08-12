# -*- coding:utf-8 -*-

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
RNN 的 意思 是 ， 为了 预测 最后 的 结果 ， 我 先 用 第一个 词 预测 ， 当然 ， 只 用 第一个 预测 的 预测 结果 肯定 不 精确 ， 我 把 这个 结果 作为 特征 ， 跟 第二词 一起 ， 来 预测 结果 ； 接着 ， 我 用 这个 新 的 预测 结果 结合 第三词 ， 来 作 新 的 预测 ； 然后 重复 这个 过程 。
结婚的和尚未结婚的
苏剑林是科学空间的博主 。
广东省云浮市新兴县
魏则西是一名大学生
这 真是 不堪入目 的 环境
列夫·托尔斯泰 是 俄罗斯 一 位 著名 的 作家
保加利亚 首都 索非亚 是 全国 政治 、 经济 、 文化中心 ， 位于 保加利亚 中 西部
罗斯福 是 第二次世界大战 期间 同 盟国 阵营 的 重要 领导人 之一 。 1941 年 珍珠港 事件发生 后 ， 罗斯 福力 主对 日本 宣战 ， 并 引进 了 价格 管制 和 配给 。 罗斯福 以 租 借 法案 使 美国 转变 为 “ 民主 国家 的 兵工厂 ” ， 使 美国 成为 同 盟国 主要 的 军火 供应商 和 融资 者 ， 也 使得 美国 国内 产业 大幅 扩张 ， 实现 充分 就业 。 二战 后期 同 盟国 逐渐 扭转 形势 后 ， 罗斯福 对 塑造 战后 世界 秩序 发挥 了 关键 作用 ， 其 影响 力 在 雅尔塔 会议 及 联合国 的 成立 中 尤其 明显 。 后来 ， 在 美国 协助 下 ， 盟军 击败 德国 、 意大利 和 日本 。
"""
print(' '.join(cut_word(s)))