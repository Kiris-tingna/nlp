# -*- coding:utf-8 -*-
# __author__ = 'wuwei'
#将所有的问答对存入MongoDB

import xlrd
import sys
import json
import pymongo
from pymongo import MongoClient


# 连接数据库
client = MongoClient('ai.great-data.com.cn', 27017)
db = client.BMTest
collection = db.QA_pairs_collection

data = xlrd.open_workbook('QAPairs.xlsx')
table = data.sheets()[0]
# 读取excel第一行数据作为存入mongodb的字段名
rowstag = table.row_values(0)
nrows = table.nrows
# ncols=table.ncols
# print rows
returnData = {}
for i in range(1, nrows):
    # 将字段名和excel数据存储为字典形式，并转换为json格式
    returnData[i] = json.dumps(dict(zip(rowstag, table.row_values(i))))
    # 通过编解码还原数据
    returnData[i] = json.loads(returnData[i])
    # print returnData[i]
    collection.insert(returnData[i])
print("知识库问答对 已成功导入MongoDB!")