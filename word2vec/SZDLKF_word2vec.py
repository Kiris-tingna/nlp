# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:SZDLKF_word2vec.py
# @time:2017/3/12 0012 18:01
import gensim
model = gensim.models.Word2Vec.load("SZDLKF_answer.segment.model")

print(model.most_similar(u"电费"))
result = model.most_similar(u"触电")
for e in result:
    print (e[0], e[1], '\n')
print(model.similarity(u"触电", u"短路"))
print (model.doesnt_match(u"电费 带电 导线 短路".split()))