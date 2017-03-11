# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:word1.py
@time:2017/3/8 0008 16:24
"""

import jieba

infile = 'news_tensite_xml.smarty.txt'
outfile = 'news_tensite_xml.smarty.cut.txt'

inp = open(infile, 'r', encoding='utf-8')
outp = open(outfile, 'w', encoding='utf8')

for line in inp.readlines():
    seg_list = jieba.lcut(line)
    line = "/ ".join(seg_list)
    print(line)
    outp.write(line)
inp.close()
outp.close()
