# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:cutword1.py
# @time:2017/8/18 0018 16:28
# http://spaces.ac.cn/archives/3908/
# 【中文分词系列】 1. 基于AC自动机的快速分词
import ahocorasick

def load_dic(dicfile):
    from math import log
    dic = ahocorasick.Automaton()
    total = 0.0
    with open(dicfile) as dicfile:
        words = []
        for line in dicfile:
            line = line.split(' ')
            words.append((line[0], int(line[1])))
            total += int(line[1])
    for i,j in words:
        dic.add_word(i, (i, log(j/total))) # 这里使用了对数概率，防止溢出
    dic.make_automaton()
    return dic

dic = load_dic('me.dic')


def all_cut(sentence):
    words = []
    for i,j in dic.iter(sentence):
        words.append(j[0])
    return words

def max_match_cut(sentence):
    sentence = sentence.decode('utf-8')
    words = ['']
    for i in sentence:
        i = i.encode('utf-8')
        if dic.match(words[-1] + i):
            words[-1] += i
        else:
            words.append(i)
    return words


def max_proba_cut(sentence):
    paths = {0:([], 0)}
    end = 0
    for i,j in dic.iter(sentence):
        start,end = 1+i-len(j[0]), i+1
        if start not in paths:
            last = max([i for i in paths if i < start])
            paths[start] = (paths[last][0]+[sentence[last:start]], paths[last][1]-10)
        proba = paths[start][1]+j[1]
        if end not in paths or proba > paths[end][1]:
            paths[end] = (paths[start][0]+[j[0]], proba)
    if end < len(sentence):
        return paths[end][0] + [sentence[end:]]
    else:
        return paths[end][0]


to_break = ahocorasick.Automaton()
for i in ['，', '。', '！', '、', '？', ' ', '\n']:
    to_break.add_word(i, i)

to_break.make_automaton()

def map_cut(sentence):
    start = 0
    words = []
    for i in to_break.iter(sentence):
        words.extend(max_proba_cut(sentence[start:i[0]+1]))
        start = i[0]+1
    words.extend(max_proba_cut(sentence[start:]))
    return words
