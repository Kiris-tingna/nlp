# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:kbase1.py
# @time:2017/3/13 0013 13:33
class KBase:
    '基类'
    KBase_count = 0

    def __init__(self, question, question_expand, answer, answer_expand):
        self.question = question
        self.answer = answer
        KBase.KBase_count += 1

    def displayCount(self):
        print("Total Employee %d" % KBase.KBase_count)

    def displayKBase(self):
        print("标准问题: ", self.question, "\n标准答案: ", self.answer)

import xlrd

workbook = xlrd.open_workbook('知识库.xlsx')
booksheet = workbook.sheet_by_name('Sheet0')

p = list()
kb = list()
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
        kb.append(KBase(row_data[0],row_data[1],row_data[2],row_data[3]))

print('Process '+ str(i))

for i in range(len(kb)) :
    kb[i].displayKBase()
