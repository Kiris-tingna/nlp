# -*- coding: UTF-8 -*-
import sys,os
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from yaha.analyse import ChineseAnalyzer 
from yaha.analyse import YahaCorrector,words_train

#copy this file from jieba project, just for testing

analyzer = ChineseAnalyzer()
str = u"我的好朋友是李明;我爱北京天安门;IBM和Microsoft;... I have a dream interesting"
for t in analyzer(str):
    print(len(t.text), t.text)

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
if not os.path.exists("tmp"):
    os.mkdir("tmp")

ix = create_in("tmp", schema) # for create new index
#ix = open_dir("tmp") # for read only
writer = ix.writer()

writer.add_document(
    title=u"document1", 
    path=u"/a",
    content=u"This is the first document we’ve added!"
)

writer.add_document(
    title=u"document2", 
    path=u"/b",
    content=u"The second one 你 中文测试中文 is even more interesting! 吃水果"
)

writer.add_document(
    title=u"document3", 
    path=u"/c",
    content=u"买水果然后来世博园。"
)

writer.add_document(
    title=u"document4", 
    path=u"/c",
    content=u"工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"
)

writer.add_document(
    title=u"document4", 
    path=u"/c",
    content=u"咱俩交换一下吧。"
)

writer.commit()
searcher = ix.searcher()
parser = QueryParser("content", schema=ix.schema)

for keyword in (u"水果世博园",u"你",u"first",u"中文",u"交换机",u"交换"):
    print("result of ",keyword)
    q = parser.parse(keyword)
    results = searcher.search(q)
    for hit in results:  
        print(hit.highlights("content"))
    print("="*10)

words_train('movie.txt', 'movie_key.txt', 'movie.graph')
cor = YahaCorrector('movie_key.txt','movie.graph')
sugs = cor.suggest(u"刘牛德")
print(" ".join(sugs))
