# -*- coding:utf-8 -*-
# __author__ = 'wuwei'
#将知识库的所有问句进行分词，并以列表的形式存入MongoDB
#形式为[[词1，词2，词3],[词1，词2，词3]...[词1，词2，词3]]
import time
start = time.time()
import jieba
import codecs
import cal_BM25
from pymongo import MongoClient

jieba.initialize()

stop_words = './stopwords.txt'
stopwords = codecs.open(stop_words,'r',encoding='utf8').readlines()
stopwords = [w.strip() for w in stopwords]

def tokenization(filename):
    corpus = []
    with open(filename, 'r' , encoding="utf-8") as f:
        num=1
        for line in f.readlines():
            result = []
            words = jieba.cut(line.strip(),cut_all=False)
            str_words=""
            for word in words:
                if word not in stopwords:
                    str_words = str_words + " " + word
                    result.append(word)


            corpus.append(result)
            # print(str(num) + str_words)
            num=num+1
    return corpus

re_corpus=tokenization("./qa_question.txt")
str_corpus=str(re_corpus)

corpus_list = []
for word in re_corpus:
    if word not in stopwords:
        corpus_list.append(word)
bm25Model = cal_BM25.BM25(corpus_list)
average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())


def connect_mongo():
	client = MongoClient("ai.great-data.com.cn",27017)
	db = client.BMTest
	collection = db.corpus_collection
	return collection


posting = {
				"corpus": str_corpus,
                "average_idf":average_idf,
                "sign":"1"


			}
collection = connect_mongo()
collection.insert(posting)
print("已有问题分词结果 成功导入MongoDB!")






