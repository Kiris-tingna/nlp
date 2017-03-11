# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:jieb_posseg1.py
@time:2017/3/8 0008 17:01
"""
import re
import jieba.posseg

infile = 'news_tensite_xml.smarty.txt'
outfile = 'news_tensite_xml.smarty.posseg.txt'

inp = open(infile, 'r', encoding='utf8')
outp = open(outfile, 'w', encoding='utf8')

for line in inp.readlines():
        print('=' * 40)
        print('4. 词性标注')
        print('-' * 40)

        outp.write('-' * 10)
        outp.write(' 词性标注')
        outp.write('-' * 10+'\n')
        words = jieba.posseg.cut(line)
        for word, flag in words:
            print('%s %s' % (word, flag))
            outp.write(word)
            outp.write(flag+'\n')

inp.close()
outp.close()