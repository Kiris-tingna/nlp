# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xlsx2xml.py
# @time:2017/3/11 0011 20:21
from __future__ import division
import xlrd
import re
import os
import sqlite3

workbook = xlrd.open_workbook('知识库.xlsx')
booksheet = workbook.sheet_by_name('Sheet0')
db_filename = 'kbase.db'
db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)
print("Opened database successfully")
if db_is_new:
    print ('Need to create schema')
else:
    print ('Database exists, assume schema does, too.')
    conn.execute('drop table if exists kbase;')

conn.execute('create table kbase (id integer primary key autoincrement, question text not null,question1 text not null,  answer text not null,  question2 text not null);')

p = list()
i = 0
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
    i = i + 1
    conn.execute("INSERT INTO kbase(question,question1,answer,question2) VALUES (?,?,?,?)", row_data)

print('Process '+ str(i))
conn.execute('CREATE INDEX qa_idx ON kbase (question);')
conn.commit()
conn.close()
