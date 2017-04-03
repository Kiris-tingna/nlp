# -*- coding: cp936 -*-
import sys
import os


# 词库矩阵,相同长度词的被放同一个列表中
def matrix(max_length):
    # max_length = 11
    mat = [[] for i in range(max_length)]
    return mat


# 建立词库以便做正向最大匹配
def BuildWordBank():
    filename = r'lexicon.txt'
    fp = open(filename, "r", encoding='utf-8')
    print("Reading File '%s'..." % filename)
    lst = []
    for line in fp:
        # print line.split()[0]
        lst.append(line.split()[0])  # 取每行的第一个单词
    lst = list(set(lst))  # 去重,顺序打乱了
    fp.close()
    mat = matrix(11)
    for w in lst:  # 根据长度分类
        #mat[len(w) / 2].append(w)
        mat.append(w)
    """
    max_length=0 #词表中最大词的长度是20*1/2=10个单字
    for w in lst:
      if len(w)>max_length:max_length=len(w)
    print max_length
    """
    return mat


# 写一元文法文件，freq是单词和频数对应的词典
def writeUnigram(freq):
    f = open('test.txt', "w")
    print("writing unigram to file..")
    for key in freq:
        f.write("%s\t%d\n" % (key, freq[key]))
    f.close()
    print("writing unigram SUCCESS!")


# 写二元文法文件
def writeBigram(freq):
    f = open('bigram.txt', "w")
    print("writing bigram to file..")
    for key in freq:
        f.write("%s\t%d\n" % (key, freq[key]))
    f.close()
    print("writing bigram SUCCESS!")


# 给定词典d做MM分词,例如d[3]是全部长度为3的单词的列表
def MM(d):
    dirx = u"corpus96/"
    file_list = os.listdir(dirx)
    # print len(file_list)
    # return
    freq = {}  # 记录词和频数的一一对应
    for filename in file_list:
        # filename = "960101.TXT"
        fp = open(dirx + filename, "r")
        print        ("processing %s ,please wait.." % filename)
        iters = 1  # 记录迭代行数
        for line in fp.readlines():
            if iters % 100 == 0:
                print("lines:%d" % iters)  # 输出直观
            # if iters>=20:break
            iters = iters + 1
            lst = list(line)  # 原始句子序列
            if lst == []: continue  # 语料有空行则跳过
            # print len(lst)
            # print lst
            # 句子预处理
            i = 0
            seq = []  # 其中每个元素是一个单字
            while i < len(lst):
                if lst[i] == '\n': break
                if lst[i] in (' ', '|'):  # 遇到半字字符继续向后扫描
                    i += 1
                else:
                    # sys.stdout.write(lst[i]+lst[i+1])
                    seq.append(lst[i] + lst[i + 1])
                    i += 2
            # print seq
            # 开始MM
            Maxlen = 10  # 设置最大词长
            i = 0  # 初始化
            j = i + Maxlen
            eachline = []  # 存储每行分词后的结果,以便统计unigram和bigram
            while i < len(seq):
                if j > len(seq): j = len(seq)  # 控制右指针不能超过句子边界
                if j - i == 1:  # 单字时
                    # sys.stdout.write("".join(seq[i:j])+"\\")
                    eachline.append("".join(seq[i:j]))
                    i = j
                    j = i + Maxlen
                if "".join(seq[i:j]) in d[len(seq[i:j])]:  # 若串在词典中
                    # sys.stdout.write("".join(seq[i:j])+"\\")
                    eachline.append("".join(seq[i:j]))
                    i = j
                    j = i + Maxlen
                else:
                    j -= 1
            # sys.stdout.write("\n")
            """
            for w in eachline:  #记录一元频数
              if w in freq:freq[w]+=1
              else:freq[w]=1
            #print eachline
            for w in eachline:print w
            """
            for i in range(len(eachline)):  # 记录二元频数
                w = "".join(eachline[i:i + 2])
                if w in freq:
                    freq[w] += 1
                else:
                    freq[w] = 1
        fp.close()
        print("process %s SUCCESS!" % filename)
        # return freq
        # break  #只测试一个文件时打开
    return freq
    # 向文件写入频数,根据频数字典freq


# 主函数
dictionary = BuildWordBank()
freq = MM(dictionary)  # 正向最大匹配，返回频数字典
# print freq
# writeUnigram(freq)
writeBigram(freq)