# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:InvertedIndex.py
# @time:2017/8/1 0001 13:48
#-------------------------------------------------------------------------------
# Name:        InvertedIndex
# Purpose:     倒排索引
# Created:     02/04/2013
# Copyright:   (c) neng 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import string

# 建立倒排索引
# 输入:199801_new.txt
# 输出:my_index.txt  格式(从0开始): word (段落号,段落中位置) ..


def create_inverted_index(filename):
    # 变量说明
    sub_list = [] # 所有词的list,  用来查找去重等
    # word = []     # 词表文件
    result = {}   # 输出结果 {单词:index}
    print("读取文件%r....."%filename)
    with open(filename, encoding='utf-8') as fn:
        # 建立词表
        src_lists = fn.readlines()
        for src_list in src_lists:
            index_data, extend_data = src_list.strip().split(',')
            sub_list.extend(extend_data.strip().split(';'))
        print(len(sub_list))
        set_data = set(sub_list)  # 去重复
        print(len(set_data))
        word = list(set_data)  # set转换成list, 否则不能索引
        word.pop(0)
        print(word)
        print(len(word))
        with open('extend_item.keyword', 'w', encoding='utf8') as fn:
            for kw in word:
                fn.write(kw + '\n')
        print("处理完成!")

    extend_list = []
    # 建立索引
    for w in range(0, len(word)):
        index = []  # 记录段落及段落位置 [(段落号,位置),(段落号,位置)...]
        for i in range(0, len(src_lists)):  # 遍历所有段落
            index_data, extend_data = src_lists[i].strip().split(',')
            sub_list = extend_data.strip().split(';')
            for j in range(0, len(sub_list)):  # 遍历段落中所有单词
                if sub_list[j] == word[w]:
                    index.append((index_data, j))
                    # print("Found:", word[w], 'in', sub_list)
            result[word[w]] = index

    des_filename = "extend_item.index"
    print("正在写入文件%r....."%des_filename)
    print(result)
    writefile = open(des_filename, 'w', encoding='utf-8')
    for k in result.keys():
        writefile.writelines(str(k)+str(result[k])+"\n")
    print("处理完成!")


def main():
    create_inverted_index("extend_item.dict")


if __name__ == '__main__':
    main()