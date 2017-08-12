# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:hmm1.py
# @time:2017/8/12 0012 0:31
from collections import Counter
from math import log
import math

hmm_model = {i: Counter() for i in 'sbme'}

with open('dict_small.txt', encoding='utf-8') as f:
    for line in f:
        lines = line.split(' ')
        if len(lines[0]) == 1:
            #  single word
            hmm_model['s'][lines[0]] += int(lines[1])
        else:
            #  not single word
            hmm_model['b'][lines[0][0]] += int(lines[1])
            hmm_model['e'][lines[0][-1]] += int(lines[1])
            for m in lines[0][1:-1]:
                hmm_model['m'][m] += int(lines[1])

log_total = {i: log(sum(hmm_model[i].values())) for i in 'sbme'}

# for k, v in hmm_model.items():
#    print(k, v)

trans = {'ss': 0.3,
         'sb': 0.7,
         'bm': 0.3,
         'be': 0.7,
         'mm': 0.3,
         'me': 0.7,
         'es': 0.3,
         'eb': 0.7
         }

trans = {i: log(j) for i, j in trans.items()}
for k, v in trans.items():
    print(k, v)

def viterbi(nodes):
    paths = nodes[0]
    for l in range(1, len(nodes)):
        paths_ = paths
        paths = {}
        for i in nodes[l]:
            nows = {}
            for j in paths_:
                if j[-1]+i in trans:
                    nows[j+i] = paths_[j]+nodes[l][i]+trans[j[-1]+i]
            k = list(nows.values()).index(max(list(nows.values())))
            paths[list(nows.keys())[k]] = list(nows.values())[k]
    return list(paths.keys())[list(paths.values()).index(max(list(paths.values())))]

def hmm_cut(s):
    nodes = [{i:log(j[t]+1)-log_total[i] for i, j in hmm_model.items()} for t in s]
    tags = viterbi(nodes)
    words = [s[0]]
    for i in range(1, len(s)):
        if tags[i] in ['b', 's']:
            words.append(s[i])
        else:
            words[-1] += s[i]
    return words

# 今天 天气 不错
print(' '.join(hmm_cut('今天天气不错')))
#print('今天 天气 不错')
# 李想 是 一个 好 孩子
print(' '.join(hmm_cut('李想是一个好孩子')))
#print('李想 是 一个 好 孩子')
# 小明 硕士 毕业 于 中 国科 学院 计算 所
print(' '.join(hmm_cut('小明硕士毕业于中国科学院计算所')))
#print("小明 硕士 毕业 于 中 国科 学院 计算 所")
print(' '.join(hmm_cut('已结婚的和尚未结婚的青年都要实行计划生育')))