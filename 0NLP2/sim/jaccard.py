#!/usr/local/bin/python
# -*- coding:utf-8 -*-
#Date:2016.6.13
#用法：计算两个关键词之间的相似度。
import requests,time,random,pycurl,json,datetime,re,threading,urllib
import os
# from urlparse import *
from hashlib import md5
from multiprocessing.dummy import Pool as ThreadPool 
import codecs	#为了生成gbk编码的文件
from lxml import etree
import jieba
today = datetime.date.today()

# import MySQLdb as mdb
# import xlsxwriter as wx
# from lxml import etree
# import xlrd

import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


def jaccard(a,b):    
    c=[v for v in a if v in b]    
    return float(len(c))/(len(a)+len(b)-len(c))  

c = 0
k1list = []
k2list = []
for k1 in open("k1.txt"):
	k1 = k1.strip()
	k1list.append(k1)

for k2 in open("k2.txt"):
	k2 = k2.strip()
	k2list.append(k2)

for k1 in k1list:	
	c += 1	
	k1 = k1.strip()
	f = open("ok.txt","a")
	f.write("%s\t%s\n"%(c,k1))
	f.flush()
	# text = k1
	# seg_list1 = jieba.cut(k1)
	# seg_list2 = jieba.cut_for_search(k1)	
	# print u"[精确模式]: ", "/ ".join(seg_list1)
	# print u"[搜索引擎模式]: ", "/ ".join(seg_list2)
	# time.sleep(3)
	c2 = 0
	for k2 in k2list:
		c2 += 1
		k2 = k2.strip()
		print("%s,%s,%s,%s"%(c,k1,c2,k2))
		if jaccard(k1,k2) > 0.6:
			print(jaccard(k1,k2))
			f.write("%s\t%s\t%s\n"%(k1,k2,jaccard(k1,k2)))
			f.flush()
			# time.sleep(3)
