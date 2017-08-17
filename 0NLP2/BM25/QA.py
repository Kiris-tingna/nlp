# -*- coding:utf-8 -*-
# __author__ = 'wuwei'
import time
import jieba
import codecs
import cal_BM25
from pymongo import MongoClient

#提取MongoDB中的所有问题的分词结果
def select_corpus():
    client = MongoClient("ai.great-data.com.cn",27017)
    db = client.BMTest
    collection = db.corpus_collection
    send_corpus = []
    for res in collection.find({"sign": "1"}):
        res_corpus = res["corpus"]
        send_corpus = list(eval(res_corpus))
        break
    return send_corpus

def select_average_idf():
    client = MongoClient("ai.great-data.com.cn",27017)
    db = client.BMTest
    collection = db.corpus_collection
    for res in collection.find({"sign": "1"}):
        rcv_idf = res["average_idf"]
        break
    return rcv_idf

#根据索引提取出对应的答案
def select_answer(idx):
    client = MongoClient("ai.great-data.com.cn", 27017)
    db = client.BMTest
    collectionc = db.QA_pairs_collection
    for resc in collectionc.find({"编号": "编号" + str(idx + 1)}):
        res_ans = resc["答案"]
        print(res_ans)
        break

#问答处理过程
def QA_process(query_str,bm25Model,average_idf):
    scores = bm25Model.get_scores(query_str, average_idf)
    print(scores)
    maxv = 0
    for sc in scores:
        if sc > maxv:
            maxv = sc
    print("BM25最大值:" + str(maxv))
    idx = scores.index(max(scores))
    print("序号:" + str(idx + 1))
    select_answer(idx)

#主方法
def main_run():
    stop_words = './stopwords.txt'
    stopwords = codecs.open(stop_words, 'r', encoding='utf8').readlines()
    stopwords = [w.strip() for w in stopwords]
    jieba.initialize()
    print("")
    rcv_send_sorpus=select_corpus()
    bm25Model = cal_BM25.BM25(rcv_send_sorpus)
    average_idf = select_average_idf()
    while True:
        query_str = input("\n请输入您的问题：")
        start = time.time()
        words = jieba.cut(query_str.strip(), cut_all=False)
        search_txt = []
        for word in words:
            if word not in stopwords:
                search_txt.append(word)

        QA_process(search_txt,bm25Model,average_idf)

        # 输出回答当前问题的运行时间
        print(search_txt)
        end = time.time()
        print("Time cost:" + str(end - start))




if __name__ == '__main__':
    main_run()

