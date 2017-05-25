# coding:utf-8
from gensim import corpora,similarities,models
import os
import jieba

# 首先加载语料库
if os.path.exists('lsi_corpus.mm') and os.path.exists('mydict.dic'):
    dictionary = corpora.Dictionary.load('mydict.dic')
    corpus = corpora.MmCorpus('lsi_corpus.mm')
    model = models.LsiModel.load('model.lsi')
    print('used files generated from topics')
else:
    print('please run topics firstly')

index = similarities.MatrixSimilarity(corpus)
index.save('lsi_similarity.sim')

document = '反光照片基本作废'
bow_vec = dictionary.doc2bow(jieba.lcut(document))
lsi_vec = model[bow_vec]
sims = index[lsi_vec]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)