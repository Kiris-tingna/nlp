#!/usr/bin/env python
# coding:utf-8
class LanguageModel(object):
  def __init__(self, corpus_file):
    self.words = []
    self.freq = {}
    print ('loading words')
    with open(corpus_file,'r') as f:
      line = f.readline().strip()
      while line:
        self.words.append('<s>')
        self.words.extend(line.split())
        self.words.append('</s>')
        line = f.readline().strip()
    print ('hashing bi-gram keys')
    for i in range(1,len(self.words)):
      # 条件概率
      key = self.words[i] + '|' + self.words[i-1]
      if key not in self.freq:
        self.freq[key] = 0
      self.freq[key] += 1
    print ('hashing single word keys')
    for i in range(0,len(self.words)):
      key = self.words[i]
      if key not in self.freq:
        self.freq[key] = 0
      self.freq[key] += 1
  def get_trans_prop(self, word, condition):
    """获得转移概率"""
    key = word + '|' + condition
    if key not in self.freq:
      self.freq[key] = 0
    if condition not in self.freq:
      self.freq[condition] = 0
    C_2 = (float)(self.freq[key] + 1.0)
    C_1 = (float)(self.freq[condition] + len(self.words))
    return C_2/C_1
  def get_init_prop(self, word):
    """获得初始概率"""
    return self.get_trans_prop(word,'<s>')
  def get_prop(self, *words):
    init = self.get_init_prop(words[0])
    product = 1.0
    for i in range(1,len(words)):
      product *= self.get_trans_prop(words[i],words[i-1])
    return init*product
def main():
    lm = LanguageModel('RenMinData.txt')
    print ('total words: ', len(lm.words))
    print ('total keys: ', len(lm.freq))
    print ('P(各族|全国) = ', lm.get_trans_prop('各族','全国'))
    print ('P(党|坚持) = ', lm.get_trans_prop('党','坚持'))
    print ('P(以来|建国) = ', lm.get_trans_prop('以来','建国'))
    print ('init(全国) = ', lm.get_init_prop('全国'))
    print ("P('全国','各族','人民')", lm.get_prop('全国','各族','人民'))
if __name__ == '__main__':
    main()