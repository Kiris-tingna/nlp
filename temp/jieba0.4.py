# encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")
import jieba.analyse

'''
print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
# 如果/放到/post/中将/出错/。
print(jieba.suggest_freq(('中', '将'), True))
# 494
print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
# 如果/放到/post/中/将/出错/。
print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
# 「/台/中/」/正确/应该/不会/被/切开
print(jieba.suggest_freq('台中', True))
# 69
print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
# 「/台中/」/正确/应该/不会/被/切开
'''

if __name__ == "__main__":
    jieba.suggest_freq(('审批人',), True)
    descws = open('../it_jb4.txt', 'w', encoding='utf-8')
    with open('../IT.txt', 'r', encoding='utf-8') as src:
        for sentence in src:
            print(sentence)
            seg_list = jieba.cut(sentence, HMM = False)
            segment = "/".join(seg_list)
            descws.write(segment)
            print("Segment: ", segment)
    descws.close()
