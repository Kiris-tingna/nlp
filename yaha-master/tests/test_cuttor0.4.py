# -*- coding=utf-8 -*-
import sys, re, codecs
from yaha.analyse import extract_keywords, near_duplicate, summarize1, summarize2, summarize3

#test: Get key words from file
def key_word_test():
    filename = 'question.txt'
    with codecs.open(filename, 'r', 'utf-8') as file:
        for i in range(50):
            content = file.readline()
            keys = extract_keywords(content)
            print(content)
            print('=' * 20, 'Keyword', '=' * 20)
            print(','.join(keys))
            # print('=' * 20, 'summarize1', '=' * 20)
            # print(summarize1(content))
            # print('=' * 20, 'summarize2', '=' * 20)
            # print(summarize2(content))
            # print('=' * 20, 'summarize3', '=' * 20)
            # print(summarize3(content))
            print('*' * 50, )

key_word_test()
