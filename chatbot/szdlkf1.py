# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:xlsxshow.py
@time:2017/3/7 0007 23:03
"""
import xlrd
import re

workbook = xlrd.open_workbook('知识库.xlsx')
booksheet = workbook.sheet_by_name('Sheet0')
outp = open('SZDLKF_dialogue.txt', 'w', encoding='utf8')

p = list()
i = 0
for row in range(booksheet.nrows):
    row_data = []
    for col in range(booksheet.ncols):
        cel = booksheet.cell(row, col)
        val = cel.value
        try:
            val = cel.value
            val = re.sub(r'\s+', '', val)
        except:
            pass

        if type(val) == float:
            val = int(val)
        else:
            val = str(val)
        row_data.append(val)
    p.append(row_data)
    if row_data[0] != "":
        i = i + 1
        rule = re.compile(u"[^\u4e00-\u9fa5]")
        row_data[0]= rule.sub('', row_data[0])
        row_data[2] = rule.sub('', row_data[2])
        outp.write(row_data[0]+'\n'+row_data[2] + '\n')
print('Process '+ str(i))
outp.close()

import jieba

infile = 'SZDLKF_dialogue.txt'
outfile = 'SZDLKF_dialogue.segment.txt'

inp = open(infile, 'r', encoding='utf-8')
outp = open(outfile, 'w', encoding='utf8')

print('=' * 40)
print('中文分词')
print('-' * 40)
for line in inp.readlines():
    seg_list = jieba.lcut(line)
    line = "/ ".join(seg_list)
    #print(line)
    outp.write(line)
print('中文分词 OK')
inp.close()
outp.close()

# 关键词提取
import jieba.analyse
infile = 'SZDLKF_dialogue.segment.txt'
outfile = 'SZDLKF_dialogue.analyse.txt'
inp = open(infile, 'r', encoding='utf8')
outp = open(outfile, 'w', encoding='utf8')

print('=' * 40)
print('关键词提取')
print('-' * 40)
for line in inp.readlines():
    outp.write(line)
    outp.write(' TF-IDF:')
    for x, w in jieba.analyse.extract_tags(line, withWeight=True):
#        print('%s %s' % (x, w))
        outp.write(x)
        outp.write(str(w))
    outp.write('\n')
    outp.write(' TextRank:')
    for x, w in jieba.analyse.textrank(line, withWeight=True):
#        print('%s %s' % (x, w))
        outp.write(x)
        outp.write(str(w))
    outp.write('\n')
print('关键词提取OK')
inp.close()
outp.close()