# -*- coding=utf-8 -*-
import sys, re, codecs
import cProfile
from yaha.wordmaker import WordDict

re_line = re.compile("\W+|[a-zA-Z0-9]+", re.UNICODE)


def sentence_from_file(filename):
    with codecs.open(filename, 'r', 'utf-8') as file:
        for line in file:
            for sentence in re_line.split(line):
                yield sentence


def make_new_word(file_from, file_save):
    word_dict = WordDict()
    word_dict.add_user_dict('www_qq0')
    for sentence in sentence_from_file(file_from):
        word_dict.learn(sentence)
    word_dict.learn_flush()
    
    str = '我们的读书会也顺利举办了四期'
    seg_list = word_dict.cut(str)
    print(', '.join(seg_list))

    word_dict.save_to_file(file_save)


# 最大熵算法得到新词
def test():
    make_new_word('../readme.md', 'www_qq0')
    cProfile.run('test()')

test()
