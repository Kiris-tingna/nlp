# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 17:40:16 2016

@author: lkh
"""

import codecs
import string
import numpy as np
import struct
import math
'''
加载google词向量
'''
def load_word2vec(fn,encoding='utf-8',regular=True):
    
    #fd=codecs.open(fn,'rb','utf-8')
    fd = open(fn,'rb')
    line = fd.readline()
    ws,s = line.split()
    ws =string.atoi(ws)
    s=string.atoi(s)

    w2v={}

    for i in range(ws):
        word=''
        while True:
            b = fd.read(1)
            if b!=' ' and b!='\r' and b!='\n' : word+=b
            else : break
        word=word.decode(encoding)
        
        vect=[]
        leng=0.0
        for j in range(s):
            vj=fd.read(4)
            try:
                vj,=struct.unpack('f',vj)
            except:
                print(i,j,vj)
                vj=0.0
                
            vect.append(vj)
            if regular :leng+=vj*vj
            
        #for i in xrange(len(vect)) : vect[i]=vect[i]/leng:
        v=np.array(vect)
        if regular : v=v/math.sqrt(leng)# 原始C程序，做了开方处理
        w2v[word]=v
        
        fd.read(1)
        
    fd.close()#换行
    
    return w2v


'''
'''
def add_topn(l,v,top=10):
    index=len(l);
    for i,val in enumerate(l):
        if v>val:
            index=i
            break
    if index<top:
        l.insert(index,v)
        if len(l) > top :del l[top]
    return index


'''
words可以是多个词，若是，vect是多个词的词向量相加

1 先求自己的长度
2 循环所有的词向量
    如果是要求的词，跳过
    不是，计算距离，简单矢量相乘
'''
def NearestN(allvect,words,vect,topn=40):
    ws=[]
    ds=[]
    for k,v in allvect.items():
        if k in words: continue
        d=vect.dot(v.T)
        index=add_topn(ds,d,topn)
        ws.insert(index,k)
        if len(ws)>topn: del ws[topn]
    return [(word,dist) for word,dist in zip(ws,ds)]


def distance(allvect,words,topn=40):
    v=None    
    for w in words:
        vw=None
        try:vw=allvect[w]
        except Exception: None
        if vw == None :continue
        if v==None : v=vw.copy()
        else: v=np.add(v,vw)
    if v==None: return []
    else: 
        d=v.dot(v.T)
        d=math.sqrt(d)
        v=v/d
        return NearestN(allvect,words,v,topn)

def analogy(allvect,words,topn=40):
    if len(words)<3: return []
    v0=None
    try:v0=allvect[words[0]]
    except Exception: return []
    
    v1=None
    try:v1=allvect[words[1]]
    except Exception: return []
    
    v2=None
    try:v2=allvect[words[2]]
    except Exception: return []
    
    v=np.add(v1,-v0)
    v=np.add(v,v2)
    
    d=v.dot(v.T)
    d=math.sqrt(d)
    v=v/d
    
    return NearestN(allvect,words,v,topn)
'''
v=None
for w in words:
    vw=None
    try:vw=w2c[w]
    except Exception: None
    if vw == None :continue
    if v==None : v=vw.copy(vw)
    else: v=np.add(v,vw)
'''


#ifd = codecs.open("C:/tools/msys64/home/lkh/news_tensite_xml.dat", 'rb','gb18030')#gbk
#ifd = open("C:/tools/msys64/home/lkh/news_tensite_xml.dat", 'rb')
#ofd = codecs.open("C:/tools/msys64/home/lkh/corpus.txt",'wb','utf-8')

import re
import jieba

def sougou_corpus_preprocess(ifn,ofn,iencoding='gb18030',oencoding='tuf-8'):
    ifd=codecs.open(ifn,'rb',iencoding)
    ofd=codecs.open(ofn,'wb',oencoding)

    pt = re.compile(r'<contenttitle>(.*)</contenttitle>')
    pc = re.compile(r'<content>(.*)</content>')

    i=0
    line = ifd.readline()#.decode('gb18030')

    while line:
        txt=None
        m = re.match(pt,line)
        if m : txt=m.groups()[0]#ofd.write(m.groups()[0])
        else :
            m = re.match(pc,line)
            if m : txt=m.groups()[0]#ofd.write(m.groups()[0])
    
        if txt: 
            ofd.write(' '.join(jieba.cut(txt)))
            ofd.write('\n')
        
        i+=1
        if i% 1000 == 0: print('.',)
        
        #if i > 1000: break
        
        try:
            line = ifd.readline()#.decode('gb18030')
        except Exception:
            print(i)
        
    ifd.close()
    ofd.close()

