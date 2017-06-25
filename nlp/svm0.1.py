# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:svm0.1.py
# @time:2017/6/25 0025 10:43
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 PPMessage.
# Guijin Ding, dingguijin@gmail.com
#

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC

import jieba

def _classification():
    _target = []
    _data1 = ["您好", "你多大了", "你是什么呀", "你怎么了", "你男的女的呀"]
    _target.append("我是PPMessage智能客服，我的名字叫PP，我很面，就是一个小PP，所以叫PP，您有什么的问题需要问我？")

    _data2 = ["我想买", "怎么部署PPMESSAGE", "怎么下载PPMessage", "ppmessage是什么意思"]
    _target.append("这个问题涉及到我们的核心利益 ^_^，转人工客服吧？")

    _X = []
    _Y = []
    for _data in _data1:
        _X.append(" ".join(jieba.lcut(_data)))
        _Y.append(0)

    for _data in _data2:
        _X.append(" ".join(jieba.lcut(_data)))
        _Y.append(1)

    _v = TfidfVectorizer()
    _X = _v.fit_transform(_X)

    _clf = SVC(C=1000000.0, gamma='auto', kernel='rbf')
    _clf.fit(_X, _Y)

    _data = "PPMessage"
    _x = " ".join(jieba.lcut(_data))
    _x = _v.transform([_x])
    _y = _clf.predict(_x)
    print(_target[_y[0]])
    return

if __name__ == "__main__":
    _classification()