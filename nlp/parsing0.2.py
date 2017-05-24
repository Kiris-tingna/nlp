# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:parsing0.1.py
# @time:2017/5/18 0018 15:10

# python3
from pyparsing import *
kw = CaselessKeyword( '电费' )
hello = "请查询上个月的电费"
st=SkipTo(kw)
st.parseString(hello)
print (hello, "->", st.parseString(hello))