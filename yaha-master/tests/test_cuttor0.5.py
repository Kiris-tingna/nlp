# -*- coding=utf-8 -*-
import sys, re, codecs
from yaha.analyse import extract_keywords, near_duplicate, summarize1, summarize2, summarize3


# 比较文本的相似度
def compare_file():
    file1 = codecs.open('test_cuttor0.2.py', 'r', 'utf-8')
    file2 = codecs.open('test_cuttor0.1.py', 'r', 'utf-8')
    print('the near of two files is:', near_duplicate(file1.read(), file2.read()))

compare_file()
