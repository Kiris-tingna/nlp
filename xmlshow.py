# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:xmlshow.py
@time:2017/3/7 0007 22:00
"""

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

tree = ET.parse('keyword.xml')
root = tree.getroot()

keywords = root.findall('keyword')
i=0
p = list()
for keyword in keywords:
    value = keyword.find('value').text
    importance = keyword.find('importance').text
    i = i+1
    row_data = []
    #print(i,value,importance)
    row_data.append(value)
    row_data.append(importance)
    print(row_data)
    p.append(row_data)