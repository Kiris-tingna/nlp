# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:word1.py
@time:2017/3/8 0008 16:24
"""
import re
import jieba

infile = 'news_tensite_xml.smarty.dat'
outfile = 'news_tensite_xml.smarty.result.txt'

inp = open(infile, 'r', encoding='gb18030')
outp = open(outfile, 'w', encoding='utf8')
line = inp.readline()
for line in inp.readlines():
    if re.match(r'<content>.', line):
        m = re.split(r'<content>', line)
        line = m[1]
        m = re.split(r'</content>', line)
        line = m[0]
        #print(line)
        seg_list = jieba.lcut(line, cut_all=False)
        #print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
        line = "/ ".join(seg_list)
        outp.write(line)
inp.close()
outp.close()