# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:simhash0.2.py
# @time:2017/5/24 0024 16:07

import re
from simhash import Simhash, SimhashIndex
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

data = {
    1: u'How are you? I Am fine. blar blar blar blar blar Thanks.',
    2: u'How are you i am fine. blar blar blar blar blar than',
    3: u'This is simhash test.',
}
objs = [(str(k), Simhash(get_features(v))) for k, v in data.items()]
index = SimhashIndex(objs, k=3)

print(index.bucket_size())

s1 = Simhash(get_features(u'How are you i am fine. blar blar blar blar blar thank'))
print(index.get_near_dups(s1))

index.add('4', s1)
print(index.get_near_dups(s1))

data = {
    1: '如何 打开 GIS 中 设备树?',
    2: '如何 在GIS 中 打开 设备树',
    3: '如何 关闭 GIS 中 设备树',
}
objs = [(str(k), Simhash(get_features(v))) for k, v in data.items()]
index = SimhashIndex(objs, k=3)

print(index.bucket_size())

s1 = Simhash(get_features(u'如何 打开 GIS 中 设备树'))
print(index.get_near_dups(s1))

index.add('4', s1)
print(index.get_near_dups(s1))