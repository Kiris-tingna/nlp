# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:nltk.py
@time:2017/3/8 0008 12:19
"""
import nltk
from urllib3 import urlopen


url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = urlopen(url).read()
raw = nltk.clean_html(html)
print(raw)