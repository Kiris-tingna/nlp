#coding:utf-8
from gensim import corpora,similarities,models
import os

# 首先加载语料库
if os.path.exists('mydict.dic') and os.path.exists('corpus.mm'):
    dictionary = corpora.Dictionary.load('mydict.dic')
    corpus = corpora.MmCorpus('corpus.mm')
    print ('used files generated from string2vector')
else:
    print ('please run string2vector firstly')


#创建一个model
tfidf = models.TfidfModel(corpus=corpus)
tfidf.save('model.tfidf')
#使用创建好的model生成一个对应的向量
vector = tfidf[corpus[0]]
print(vector)
#序列化
tfidf_corpus = tfidf[corpus]
corpora.MmCorpus.serialize('tfidf_corpus.mm', tfidf_corpus)

#lsi
lsi = models.LsiModel(corpus = tfidf_corpus,id2word=dictionary,num_topics=2)
lsi_corpus = lsi[tfidf_corpus]
lsi.save('model.lsi')
corpora.MmCorpus.serialize('lsi_corpus.mm', lsi_corpus)
print ('LSI Topics:')
print (lsi.print_topics(20))

#lda
lda = models.LdaModel(corpus = tfidf_corpus,id2word=dictionary,num_topics=2)
lda_corpus = lda[tfidf_corpus]
lda.save('model.lda')
corpora.MmCorpus.serialize('lda_corpus.mm', lda_corpus)
print ('LDA Topics:')
print (lda.print_topics(20))