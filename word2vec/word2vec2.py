# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:word2vec2.py
# @time:2017/3/12 0012 17:21

from gensim.models import Word2Vec, LdaModel


class MyCorpus(object):
    def __init__(self, docs):
        self.docs = docs

    def __iter__(self):
        for line in self.docs:
            yield line.split()


f1 = open(r'../chatbot/SZDLKF_answer.segment.txt', 'r', encoding='utf8')
outp1 = open(r'model', 'a+')
outp2 = open(r'model_vec', 'a+')

if __name__ == "__main__":
    corpuss = MyCorpus(f1)

    model = Word2Vec(corpuss, size=20, window=5, min_count=0)
    model.save(outp1)
    model.save_word2vec_format(outp2, binary=False)
    # print model["obama"]
    # print model.similarity('obama', 'speech')

f1.close()
outp1.close()
outp2.close()