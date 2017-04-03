# -*- coding: cp936 -*-
import sys
import os


# �ʿ����,��ͬ���ȴʵı���ͬһ���б���
def matrix(max_length):
    # max_length = 11
    mat = [[] for i in range(max_length)]
    return mat


# �����ʿ��Ա����������ƥ��
def BuildWordBank():
    filename = r'lexicon.txt'
    fp = open(filename, "r", encoding='utf-8')
    print("Reading File '%s'..." % filename)
    lst = []
    for line in fp:
        # print line.split()[0]
        lst.append(line.split()[0])  # ȡÿ�еĵ�һ������
    lst = list(set(lst))  # ȥ��,˳�������
    fp.close()
    mat = matrix(11)
    for w in lst:  # ���ݳ��ȷ���
        #mat[len(w) / 2].append(w)
        mat.append(w)
    """
    max_length=0 #�ʱ������ʵĳ�����20*1/2=10������
    for w in lst:
      if len(w)>max_length:max_length=len(w)
    print max_length
    """
    return mat


# дһԪ�ķ��ļ���freq�ǵ��ʺ�Ƶ����Ӧ�Ĵʵ�
def writeUnigram(freq):
    f = open('test.txt', "w")
    print("writing unigram to file..")
    for key in freq:
        f.write("%s\t%d\n" % (key, freq[key]))
    f.close()
    print("writing unigram SUCCESS!")


# д��Ԫ�ķ��ļ�
def writeBigram(freq):
    f = open('bigram.txt', "w")
    print("writing bigram to file..")
    for key in freq:
        f.write("%s\t%d\n" % (key, freq[key]))
    f.close()
    print("writing bigram SUCCESS!")


# �����ʵ�d��MM�ִ�,����d[3]��ȫ������Ϊ3�ĵ��ʵ��б�
def MM(d):
    dirx = u"corpus96/"
    file_list = os.listdir(dirx)
    # print len(file_list)
    # return
    freq = {}  # ��¼�ʺ�Ƶ����һһ��Ӧ
    for filename in file_list:
        # filename = "960101.TXT"
        fp = open(dirx + filename, "r")
        print        ("processing %s ,please wait.." % filename)
        iters = 1  # ��¼��������
        for line in fp.readlines():
            if iters % 100 == 0:
                print("lines:%d" % iters)  # ���ֱ��
            # if iters>=20:break
            iters = iters + 1
            lst = list(line)  # ԭʼ��������
            if lst == []: continue  # �����п���������
            # print len(lst)
            # print lst
            # ����Ԥ����
            i = 0
            seq = []  # ����ÿ��Ԫ����һ������
            while i < len(lst):
                if lst[i] == '\n': break
                if lst[i] in (' ', '|'):  # ���������ַ��������ɨ��
                    i += 1
                else:
                    # sys.stdout.write(lst[i]+lst[i+1])
                    seq.append(lst[i] + lst[i + 1])
                    i += 2
            # print seq
            # ��ʼMM
            Maxlen = 10  # �������ʳ�
            i = 0  # ��ʼ��
            j = i + Maxlen
            eachline = []  # �洢ÿ�зִʺ�Ľ��,�Ա�ͳ��unigram��bigram
            while i < len(seq):
                if j > len(seq): j = len(seq)  # ������ָ�벻�ܳ������ӱ߽�
                if j - i == 1:  # ����ʱ
                    # sys.stdout.write("".join(seq[i:j])+"\\")
                    eachline.append("".join(seq[i:j]))
                    i = j
                    j = i + Maxlen
                if "".join(seq[i:j]) in d[len(seq[i:j])]:  # �����ڴʵ���
                    # sys.stdout.write("".join(seq[i:j])+"\\")
                    eachline.append("".join(seq[i:j]))
                    i = j
                    j = i + Maxlen
                else:
                    j -= 1
            # sys.stdout.write("\n")
            """
            for w in eachline:  #��¼һԪƵ��
              if w in freq:freq[w]+=1
              else:freq[w]=1
            #print eachline
            for w in eachline:print w
            """
            for i in range(len(eachline)):  # ��¼��ԪƵ��
                w = "".join(eachline[i:i + 2])
                if w in freq:
                    freq[w] += 1
                else:
                    freq[w] = 1
        fp.close()
        print("process %s SUCCESS!" % filename)
        # return freq
        # break  #ֻ����һ���ļ�ʱ��
    return freq
    # ���ļ�д��Ƶ��,����Ƶ���ֵ�freq


# ������
dictionary = BuildWordBank()
freq = MM(dictionary)  # �������ƥ�䣬����Ƶ���ֵ�
# print freq
# writeUnigram(freq)
writeBigram(freq)