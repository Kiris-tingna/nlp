# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:doc2sim1.py
# @time:2017/5/9 0009 21:47
from gensim import corpora
from gensim.similarities import Similarity
import jieba
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 训练样本
raw_documents = []
with open("../FAQ.txt", 'r', encoding='utf-8') as src:
    for inline in src:
        raw_documents.append(inline)
print(len(raw_documents))
corpora_documents = []
for item_text in raw_documents:
    item_str = list(jieba.cut(item_text))
    corpora_documents.append(item_str)

# 生成字典和向量语料
dictionary = corpora.Dictionary(corpora_documents)
dictionary.save('FAQ.dict')
# print(dictionary.token2id)

# 生成语料库
corpus = [dictionary.doc2bow(text) for text in corpora_documents]
# 序列化
corpora.MmCorpus.serialize('FAQ_corpus.mm', corpus)
# 重新加载预料
new_corpus = corpora.MmCorpus('FAQ_corpus.mm')
print(len(new_corpus))
# print(corpus)
# print(list(corpus))
# for doc in corpus:
#    print(doc)

similarity = Similarity('FAQ-Similarity-index', corpus, num_features=400)

test_data_1 = '如何在一体化GIS系统中定位设备'
test_cut_raw_1 = list(jieba.lcut(test_data_1))
test_corpus_1 = dictionary.doc2bow(test_cut_raw_1)
similarity.num_best = 5
print(test_data_1)
print(test_cut_raw_1)
print(test_corpus_1)
print(similarity[test_corpus_1])  # 返回最相似的样本材料,(index_of_document, similarity) tuples

print('################################')

test_data_2 = '如何在一体化GIS系统中查看配电站的基本参数信息'
test_cut_raw_2 = list(jieba.lcut(test_data_2))
test_corpus_2 = dictionary.doc2bow(test_cut_raw_2)
similarity.num_best = 5
print(test_data_2)
print(test_cut_raw_2)
print(test_corpus_2)
print(similarity[test_corpus_2])  # 返回最相似的样本材料,(index_of_document, similarity) tuples

