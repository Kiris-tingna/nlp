# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:doc2sim1.py
# @time:2017/5/9 0009 21:47
from gensim import corpora
from gensim.similarities import Similarity
import jieba

# 训练样本
raw_documents = []
with open("IT_Q.txt", 'r', encoding='utf-8') as src:
    for inline in src:
        raw_documents.append(inline)
corpora_documents = []
for item_text in raw_documents:
    item_str = list(jieba.cut(item_text))
    corpora_documents.append(item_str)

# 生成字典和向量语料
dictionary = corpora.Dictionary(corpora_documents)
corpus = [dictionary.doc2bow(text) for text in corpora_documents]

similarity = Similarity('-Similarity-index', corpus, num_features=400)

test_data_1 = '如何在一体化GIS系统中定位设备'
test_cut_raw_1 = list(jieba.cut(test_data_1))
test_corpus_1 = dictionary.doc2bow(test_cut_raw_1)
similarity.num_best = 2
print(test_data_1)
print(test_cut_raw_1)
print(test_corpus_1)
print(similarity[test_corpus_1])  # 返回最相似的样本材料,(index_of_document, similarity) tuples

print('################################')

test_data_2 = '如何在一体化GIS系统中查看配电站的基本参数信息'
test_cut_raw_2 = list(jieba.cut(test_data_2))
test_corpus_2 = dictionary.doc2bow(test_cut_raw_2)
similarity.num_best = 3
print(test_data_2)
print(test_cut_raw_2)
print(test_corpus_2)
print(similarity[test_corpus_2])  # 返回最相似的样本材料,(index_of_document, similarity) tuples

