# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:jieba1.py
@time:2017/3/8 0008 15:18
"""
import jieba

inp = open('news.sohunews.010806.dat', 'r', encoding='utf-8')
outp = open('news.sohunews.010806.result.txt', 'w', encoding='utf8')

for line in inp.readlines():
    seg_list = jieba.lcut(line, cut_all=False)
   #print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    line = "/ ".join(seg_list)
    outp.write(line)
inp.close()
outp.close()