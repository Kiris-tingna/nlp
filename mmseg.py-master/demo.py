# -*- coding: utf-8 -*-

from codecs import open
from math import log

from lexicon import *
from segment import *


def wrap(line):
    w, f, _ = line.strip().split(' ')
    f = log(float(f) + 1.0)
    return (w, f)


with open('../dict/dict.txt', 'r', 'utf-8') as fin:
    tf = dict(map(wrap, fin))
    lex = Lexicon(tf)
    seg = Segmenter(lex)
    result = seg.segment(u'這是一隻可愛的小花貓')
    print('/'.join(result).encode('utf-8'))
