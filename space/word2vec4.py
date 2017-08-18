# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:word2vec4.py
# @time:2017/8/18 0018 16:15
# http://kexue.fm/archives/4368/
# 【不可思议的Word2Vec】 4.不一样的“相似”
import numpy as np
import gensim
model = gensim.models.word2vec.Word2Vec.load('word2vec_wx')

def predict_proba(oword, iword):
    iword_vec = model[iword]
    oword = model.wv.vocab[oword]
    oword_l = model.syn1[oword.point].T
    dot = np.dot(iword_vec, oword_l)
    lprob = -sum(np.logaddexp(0, -dot) + oword.code*dot)
    return lprob

from collections import Counter
def relative_words(word):
    r = {i:predict_proba(i, word)-np.log(j.count) for i,j in model.wv.vocab.iteritems()}
    return Counter(r).most_common()

from collections import Counter
def relative_words(word):
    r = {i:predict_proba(i, word)-0.9*np.log(j.count) for i,j in model.wv.vocab.iteritems()}
    return Counter(r).most_common()

