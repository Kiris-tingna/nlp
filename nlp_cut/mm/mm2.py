#!/usr/bin/env python
# encoding: utf-8
# -*- coding: UTF-8 -*-

import os
import sys

def get_trie(filepath):
    trie = {}
    reader = open(filepath, 'r')
    for line in reader:
        try:
            p = trie
            encodeLine = line.decode('gbk')
            sentence = encodeLine.split('\t')[0].strip()
            for word in sentence:
                if word not in p:
                    p[word] = {}
                p = p[word]
            p[None] = {}
        except Exception:
            print(line, err)
            continue
    reader.close()
    return trie

def inTrie(trie, sentence):
    p = trie
    for word in sentence:
        if word not in p:
            return False
        p = p[word]
    if not p or None in p:
        return True
    return False

#正向最大匹配算法
def ForwardMMSeg(sentence, trie, maxLen = 0):
    pdb.set_trace()
    if not isinstance(sentence, unicode):
        print ("input must be unicode")
    if maxLen == 1:
        return [word for word in sentence]
    result = []
    while len(sentence) != 0:
        if len(sentence) == 1:
            result.append(sentence)
            break
        if maxLen == 0:
            preWord = sentence
        else:
            preWord = sentence[:maxLen]
        while preWord:
            if len(preWord) == 1:
                result.append(preWord)
                break
            if inTrie(trie, preWord):
                result.append(preWord)
                break
            else:
                preWord = preWord[:-1]
        sentence = sentence.replace(preWord, u'', 1)
    return result


#逆向最大匹配算法
def ReverseMMSeg(sentence, trie, maxLen = 0):
    if not isinstance(sentence, unicode):
        print("input must be unicode")
    if maxLen == 1:
        return [word for word in sentence]
    result = []
    while len(sentence) != 0:
        if len(sentence) == 1:
            result.append(sentence)
            break
        if maxLen == 0:
            preWord = sentence
        else:
            preWord = sentence[-maxLen:]
        while preWord:
            if len(preWord) == 1:
                result.append(preWord)
                break
            if inTrie(trie, preWord):
                result.append(preWord)
                break
            else:
                preWord = preWord[1:]
        sentence = sentence[::-1].replace(preWord[::-1], u'', 1)[::-1]
    return result[::-1]



if __name__ == '__main__':
    pdb.set_trace()
    trie = get_trie(sys.argv[1])
    pdb.set_trace()
    print(ForwardMMSeg(u'单机游戏，中文输入法, 水灵儿她出污泥而不染', trie, maxLen = 10)) # ['单机游戏', '中文输入法', '水灵儿', '她', '出污泥而不染']
    print(ForwardMMSeg(u'天降大任于斯人也必先苦其心志劳其筋骨饿其体肤空乏其身行指乱其所为所以动心忍性曾益其所不能', trie, maxLen = 5)) #['天降大任','于', '斯人也', '必先', '苦', '其心', '志', '劳', '其', '筋骨', '饿', '其', '体', '肤', '空乏', '其身','行', '指', '乱', '其所', '为', '所以', '动心忍性', '曾益', '其所', '不能']
    print(ForwardMMSeg(u'结婚的和尚未结婚的', trie, maxLen = 5)) #['结婚', '的', '和尚', '未', '结婚', 的']
    print(ReverseMMSeg(u'结婚的和尚未结婚的', trie, maxLen = 5)) #['结婚', '的', '和', '尚未', '结婚', '的']