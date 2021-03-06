# -*- coding: utf-8 -*-
from tqdm import *


def gen_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, freq, _ = line.strip().split()
            dictionary_seg[word] = int(freq)
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def gen_dict1(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            dictionary_seg[word] = len(line)
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def mmcut(sentence, wordsdict, RMM=True):
    result_s = ""
    s_length = len(sentence)
    if not RMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict or w_length == 1:
                    result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                else:
                    word = word[:w_length - 1]
                w_length = w_length - 1
            s_length = len(sentence)
    else:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict or w_length == 1:
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


def mmcut2(sentence, wordsdict1, wordsdict2, RMM=True):
    result_s = ""
    s_length = len(sentence)
    if not RMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict1 or w_length == 1:
                    result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict2 or w_length == 1:
                    result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                else:
                    word = word[:w_length - 1]
                w_length = w_length - 1
            s_length = len(sentence)
    else:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict1 or w_length == 1:
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in wordsdict2 or w_length == 1:
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


wordsdict1 = gen_dict1("keywordxml.dic")
wordsdict2 = gen_dict("../jieba.dict.utf8")
desfmm = open('question_fmm.txt', 'w', encoding='utf-8')
desrmm = open('question_rmm.txt', 'w', encoding='utf-8')

with open('question.txt', 'r', encoding='utf-8') as src:
    for j in tqdm(range(1675)):
        sentence = src.readline()
        if not sentence: break
        segfmm = []
        segrmm = []
        segfmm.append(''.join(mmcut2(sentence, wordsdict1, wordsdict2, RMM=False)))
        segrmm.append(''.join(mmcut2(sentence, wordsdict1, wordsdict2)))
        for word in segfmm:
            desfmm.write(word + '/')
        for word in segrmm:
            desrmm.write(word + '/')
desfmm.close()
desrmm.close()