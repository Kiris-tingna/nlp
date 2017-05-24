# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:baidunlp0.1.py
# @time:2017/5/24 0024 17:07
# 引入NLP SDK
from aip import AipNlp
# 定义常量
APP_ID = 'a56d68fe7fae45b786416678dd91a255'
API_KEY = 'ae26af0b7cac44b28e00dc7db0aa5335'
SECRET_KEY = '451016160efb4281bb86949cdf7c67f0'

# 初始化AipNlp对象
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

query1 = "如何打开GIS中设备树?"
query2 = "如何在GIS中打开设备树?"
query3 = "如何在GIS中关闭设备树?"

# 调用短文本相似度接口
#result1 = aipNlp.simnet(query1, query2)
#print(query1)
#print(query2)
#print(result1)

result2 = aipNlp.simnet(query1, query3)
print(query1)
print(query3)
print(result2)
