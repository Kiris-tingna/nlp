# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/13 0013 11:14
from __future__ import division
from flask import Flask,request,url_for,g,render_template
import csv
import os

from math import ceil
import xlrd
import re

workbook = xlrd.open_workbook('知识库.xlsx')
booksheet = workbook.sheet_by_name('Sheet0')
outp = open('kb.csv', 'w', encoding='utf8')

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
    if row_data[0] != "":
        i = i + 1
        rule = re.compile(u"[^\u4e00-\u9fa5]")
        row_data[0]= rule.sub('', row_data[0])
        row_data[2] = rule.sub('', row_data[2])
        outp.write(row_data[0]+', '+row_data[2] + '\n')
print('Process '+ str(i))
outp.close()

app = Flask(__name__, template_folder='')

@app.before_request
def load_csv():
    g.path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'kb.csv')

@app.route('/read_csv/page/<int:page_num>')
def read_csv(page_num):
    '''
    目标url
    http://127.0.0.1:5000/read_csv/page/1?limits=20
    '''
    # 若不指定limits默认为20
    limits = request.args.get('limits')
    if limits:
        limits = int(limits)
    else:
        limits=20

    # 根据limits和所在页数生成数据
    def show_csv(reader,page=page_num,limits=limits):
        df = []
        for row in reader:
            if page_num*limits >= reader.line_num > (page_num-1)*limits:
                df.append(row)
        return df

    # 计算页面数
    with open(g.path,'r+', encoding ='utf-8') as f:
        row_length = len(f.readlines())
        pages = int(ceil(row_length/limits))

    # 计算数据
    with open(g.path,'r+',encoding ='utf-8') as f:
        reader = csv.reader(f)
        df = show_csv(reader,page_num,limits)

    return render_template('main.html',df=df,pages=pages,page_num=page_num,limits=limits)

if '__main__' == __name__:
    app.run(debug=True)