# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:simhash0.2.py
# @time:2017/5/24 0024 16:07

from simhash import Simhash
print(Simhash('aa').distance(Simhash('bb')))
print(Simhash('aa').distance(Simhash('aa')))

print(Simhash('如何 打开 GIS 中 设备树').distance(Simhash('如何 打开 GIS 中 设备树 ?')))
print(Simhash('如何 打开 GIS 中 设备树').distance(Simhash('如何 打开 GIS 设备树')))
print(Simhash('如何 打开 GIS 中 设备树').distance(Simhash('如何 关闭 GIS 中 设备树')))