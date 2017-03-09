# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:process_sg1.py
@time:2017/3/8 0008 14:24
"""
import re

inp = open('news_tensite_xml.smarty.dat', 'r', encoding='gb18030')
outp = open('news_tensite_xml.smarty.txt', 'w', encoding='utf8')

for line in inp.readlines():
    if re.match(r'<content>.', line):
        m = re.split(r'<content>', line)
        line = m[1]
        m = re.split(r'</content>', line)
        line = m[0]

        #过滤标点符号
        rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
        line = rule.sub('', line)

        print(line)
        outp.write(line+'\n')
inp.close()
outp.close()