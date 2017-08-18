# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:cutword6.py
# @time:2017/8/18 0018 16:38
# http://spaces.ac.cn/archives/4195/
# 【中文分词系列】 6. 基于全卷积网络的中文分词

# 如果用2014人民日报语料，那么预处理代码为
import glob
import re
from tqdm import tqdm
from collections import Counter, defaultdict
import json
import numpy as np
import os

txt_names = glob.glob('./2014/*/*.txt')

pure_texts = []
pure_tags = []
stops = u'，。！？；、：,\.!\?;:\n'
for name in tqdm(iter(txt_names)):
    txt = open(name, encoding='utf-8').read()
    txt = re.sub('/[a-z\d]*|\[|\]', '', txt)
    txt = [i.strip(' ') for i in re.split('['+stops+']', txt) if i.strip(' ')]
    for t in txt:
        pure_texts.append('')
        pure_tags.append('')
        for w in re.split(' +', t):
            pure_texts[-1] += w
            if len(w) == 1:
                pure_tags[-1] += 's'
            else:
                pure_tags[-1] += 'b' + 'm'*(len(w)-2) + 'e'



# 如果用backoff2005语料，那么预处理代码为
import re
from tqdm import tqdm
from collections import Counter, defaultdict
import json
import numpy as np
import os

pure_texts = []
pure_tags = []
stops = u'，。！？；、：,\.!\?;:\n'
for txt in tqdm(open('msr_training.txt')):
    txt = [i.strip(' ').decode('gbk', 'ignore') for i in re.split('['+stops+']', txt) if i.strip(' ')]
    for t in txt:
        pure_texts.append('')
        pure_tags.append('')
        for w in re.split(' +', t):
            pure_texts[-1] += w
            if len(w) == 1:
                pure_tags[-1] += 's'
            else:
                pure_tags[-1] += 'b' + 'm'*(len(w)-2) + 'e'


ls = [len(i) for i in pure_texts]
ls = np.argsort(ls)[::-1]
pure_texts = [pure_texts[i] for i in ls]
pure_tags = [pure_tags[i] for i in ls]

min_count = 2
word_count = Counter(''.join(pure_texts))
word_count = Counter({i:j for i,j in word_count.iteritems() if j >= min_count})
word2id = defaultdict(int)
id_here = 0
for i in word_count.most_common():
    id_here += 1
    word2id[i[0]] = id_here

json.dump(word2id, open('word2id.json', 'w'))
vocabulary_size = len(word2id) + 1
tag2vec = {'s':[1, 0, 0, 0], 'b':[0, 1, 0, 0], 'm':[0, 0, 1, 0], 'e':[0, 0, 0, 1]}

batch_size = 1024

def data():
    l = len(pure_texts[0])
    x = []
    y = []
    for i in range(len(pure_texts)):
        if len(pure_texts[i]) != l or len(x) == batch_size:
            yield x,y
            x = []
            y = []
            l = len(pure_texts[i])
        x.append([word2id[j] for j in pure_texts[i]])
        y.append([tag2vec[j] for j in pure_tags[i]])