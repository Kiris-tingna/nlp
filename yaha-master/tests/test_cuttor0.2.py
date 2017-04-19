# -*- coding=utf-8 -*-
from yaha import Cuttor, RegexCutting, SurnameCutting, SurnameCutting2, SuffixCutting

cuttor = Cuttor()
str = "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"

#You can set WORD_MAX to 8 for better match
cuttor.WORD_MAX = 8

#Normal cut
seglist = cuttor.cut(str)
print('Normal cut \n%s\n' % ','.join(list(seglist)))

#All cut
seglist = cuttor.cut_all(str)
print('All cut \n%s\n' % ','.join(list(seglist)))

#Tokenize for search
print('Cut for search (term,start,end)')
for term, start, end in cuttor.tokenize(str, search=True):
    print(term, start, end)
