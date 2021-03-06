# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:simhash0.1.py
# @time:2017/5/24 0024 16:05

import re
from simhash import Simhash
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

print('%x' % Simhash(get_features('How are you? I am fine. Thanks.')).value)
print('%x' % Simhash(get_features('How are u? I am fine.     Thanks.')).value)
print('%x' % Simhash(get_features('How r you?I    am fine. Thanks.')).value)

print('%x' % Simhash(get_features('如何 打开 GIS 中 设备树')).value)
print('%x' % Simhash(get_features('如何 打开 GIS 中 设备树 ?')).value)
print('%x' % Simhash(get_features('如何 打开 GIS 设备树')).value)
print('%x' % Simhash(get_features('如何 关闭 GIS 中 设备树')).value)
