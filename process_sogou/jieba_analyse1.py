# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:wordanalyse1.py
@time:2017/3/8 0008 16:32
"""

import jieba.analyse

infile = 'news_tensite_xml.smarty.txt'
outfile = 'news_tensite_xml.smarty.analyse.txt'

inp = open(infile, 'r', encoding='utf8')
outp = open(outfile, 'w', encoding='utf8')

for line in inp.readlines():
    #outp.write(line + '\n')

    print('=' * 40)
    print('3. 关键词提取')
    print('-' * 40)
    print(' TF-IDF')
    print('-' * 40)

    outp.write('-' * 10)
    outp.write(' TF-IDF')
    outp.write('-' * 10 + '\n')
    for x, w in jieba.analyse.extract_tags(line, withWeight=True):
        print('%s %s' % (x, w))
        outp.write(x)
        outp.write(str(w) + '\n')

    print('-' * 40)
    print(' TextRank')
    print('-' * 40)

    outp.write('-' * 10)
    outp.write(' TextRank')
    outp.write('-' * 10 + '\n')
    for x, w in jieba.analyse.textrank(line, withWeight=True):
        print('%s %s' % (x, w))
        outp.write(x)
        outp.write(str(w) + '\n')

inp.close()
outp.close()
