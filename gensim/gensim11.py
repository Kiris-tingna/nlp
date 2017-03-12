#coding:utf-8
import gensim
import jieba
from gensim import corpora

infile = '..\chatbot\SZDLKF_answer.txt'
inp = open(infile, 'r', encoding='utf-8')
documents = inp.read()
texts = [jieba.lcut(document) for document in documents]
#构造字典 并 保存和加载
dictionary = corpora.Dictionary(texts)
dictionary.save('mydict.dic')
print('Tokens:Id')
print(dictionary.token2id)
new_dictionary = corpora.Dictionary.load('mydict.dic')
print(new_dictionary)

#构造新的文本并且获得他的向量
new_document = "居民用电和商业用电的不同"
new_vector = dictionary.doc2bow(jieba.lcut(new_document))
print ('the vector of "%s": （tokenid,frequency)' % new_document)
print (new_vector)

#生成语料库
corpus = [ dictionary.doc2bow(text) for text in texts]
#序列化
corpora.MmCorpus.serialize('corpus.mm', corpus)
#重新加载预料
new_corpus = corpora.MmCorpus('corpus.mm')
print(len(new_corpus))