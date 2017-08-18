# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:word2vec3.py
# @time:2017/8/18 0018 16:06
# http://kexue.fm/archives/4316/
# 【不可思议的Word2Vec】 3.提取关键词
import numpy as np
import gensim
model = gensim.models.word2vec.Word2Vec.load("word2vec_wx")


def predict_proba(oword, iword):
    iword_vec = model[iword]
    oword = model.wv.vocab[oword]
    oword_l = model.syn1[oword.point].T
    dot = np.dot(iword_vec, oword_l)
    lprob = -sum(np.logaddexp(0, -dot) + oword.code*dot)
    return lprob

from collections import Counter


def keywords(s):
    s = [w for w in s if w in model]
    ws = {w:sum([predict_proba(u, w) for u in s]) for w in s}
    return Counter(ws).most_common()

import pandas as pd # 引入它主要是为了更好的显示效果
import jieba
s = "我要查询上个月的电费"
print(pd.Series(keywords(jieba.cut(s))))
s = "供电局员工需要交电费吗"
print(pd.Series(keywords(jieba.cut(s))))
s = "用电检查的主要内容"
print(pd.Series(keywords(jieba.cut(s))))
s = "电线和变电站是否会对周围居民产生电磁辐射"
print(pd.Series(keywords(jieba.cut(s))))
s = "同个用户编号下多种抄表方式的原因"
print(pd.Series(keywords(jieba.cut(s))))
