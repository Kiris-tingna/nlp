# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:process_sg1.py
@time:2017/3/8 0008 14:24
"""
import re

inp = open('news.sohunews.010806.txt', 'r', encoding='gb18030')
outp = open('news.sohunews.010806.dat', 'w', encoding='utf8')
line = inp.readline()
for line in inp.readlines():
    if re.match(r'<content>.', line):
        m = re.split(r'<content>', line)
        line = m[1]
        m = re.split(r'</content>', line)
        line = m[0]
        #print(line)
        outp.write(line)
inp.close()
outp.close()
