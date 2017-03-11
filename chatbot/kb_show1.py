# -*- coding:utf-8 -*-
"""
@author:Eric Luo
@file:xlsxshow.py
@time:2017/3/7 0007 23:03
"""
import xlrd
import re

workbook = xlrd.open_workbook('知识库.xlsx')
booksheet = workbook.sheet_by_name('Sheet0')
p = list()
for row in range(booksheet.nrows):
    row_data = []
    for col in range(booksheet.ncols):
        cel = booksheet.cell(row, col)
        val = cel.value
        try:
            val = cel.value
            val = re.sub(r'\s+', '', val)
        except:
            pass

        if type(val) == float:
            val = int(val)
        else:
            val = str(val)
        row_data.append(val)
    p.append(row_data)
    print(row_data)