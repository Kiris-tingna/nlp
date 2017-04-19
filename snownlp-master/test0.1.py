# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from snownlp import normal
from snownlp import seg
from snownlp.summary import textrank

if __name__ == '__main__':
    des = open('question_snownlp.txt', 'w', encoding='utf-8')
    wordseg = []
    with open('question.txt', 'r', encoding='utf-8') as src:
        for inline in src:
            words = seg.seg(inline)
            wordseg.append(words)
    des.write(str(wordseg))
    des.close()

