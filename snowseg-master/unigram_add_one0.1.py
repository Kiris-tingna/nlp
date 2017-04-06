# -*- coding: UTF-8 -*-
 
import math

d = {}
log = lambda x: float('-inf') if not x else math.log(x)
prob = lambda x: d[x] if x in d else 0 if len(x)>1 else 1
 
def init(filename='../sogou.dic_utf8'):
    d['_t_'] = 0.0
    with open(filename, 'r', encoding='utf-8') as handle:
        for line in handle:
            word, freq = line.split('\t')[0:2]
            d['_t_'] += int(freq)+1
            try:
                d[word] = int(freq)+1
            except:
                d[word] = int(freq)+1
 
def solve(s):
    l = len(s)
    p = [0 for i in range(l+1)]
    t = [0 for i in range(l)]
    for i in range(l-1, -1, -1):
        p[i], t[i] = max((log(prob(s[i:i+k])/d['_t_'])+p[i+k], k)
                        for k in range(1, l-i+1))
    while p[l]<l:
        yield s[p[l]:p[l]+t[p[l]]]
        p[l] += t[p[l]]
 
if __name__ == '__main__':
    init()
    wordseg = []
    with open('../question.txt', 'r', encoding='utf-8') as src:
        for inline in src:
            wordseg.append('/'.join(list(solve(inline))))
    with open('../question_unigram1.txt', 'w', encoding='utf-8') as des:
        for word in wordseg:
            des.write(word + '  ')
