# encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")
import jieba.analyse

'''
seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式
seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 默认模式
seg_list = jieba.cut("他来到了网易杭研大厦")
print(", ".join(seg_list))
seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))
print('=' * 40)
print('2. 添加自定义词典/调整词典')
print('-' * 40)
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
    descws = open('../it_jb1.txt', 'w', encoding='utf-8')
    with open('../IT.txt', 'r', encoding='utf-8') as src:
        for sentence in src:
            print(sentence)
            seg_list = jieba.cut(sentence, cut_all=True)
            # print("Full Mode: " + "/ ".join(seg_list))
            descws.write("/".join(seg_list))
    descws.close()
