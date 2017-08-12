# -*- coding: UTF-8 -*-
'''
'''


# 判断该字符是否是中文字符（不包括中文标点）
def isChineseChar(charater):
    return 0x4e00 <= ord(charater) < 0x9fa6


# 判断是否是ASCII码
def isASCIIChar(ch):
    import string
    if ch in string.whitespace:
        return False
    if ch in string.punctuation:
        return False
    return ch in string.printable


# 切割出非中文词
def getASCIIWords(sentence):
    i = 0
    words = []
    word = ''
    print(sentence)
    for ch in sentence:
        i += 1
        if isASCIIChar(ch):
            word = word + ch
        elif word:
            words.append(word)
            word = ''
        if i == len(sentence):
            words.append(word)
        # 返回英文单词
    return words


def gen_custom_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            dictionary_seg[word] = line
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def gen_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    words = []
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            dictionary_seg[words[0]] = int(words[1])
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def fmmcut(sentence, custom_dict, wordsdict):
    sentence = sentence.strip()
    s_length = len(sentence)
    english_word = ""
    result_s = "["
    while s_length > 0:
        word = sentence
        w_length = len(word)
        while w_length > 0:
            if isASCIIChar(word[0]):
                english_word = english_word + str(word[0])
                word = word[1:]
                sentence = sentence[1:]
                w_length = len(word)
                break
            elif english_word:
                result_s += english_word + "]["
                english_word = ""
                break
            elif word in custom_dict:
                result_s += word + "]["
                sentence = sentence[w_length:]
                break
            elif word in wordsdict:
                result_s += word + "]["
                sentence = sentence[w_length:]
                break
            elif w_length == 1:
                # print(word)
                result_s += word + "]["
                sentence = sentence[w_length:]
                break
            word = word[:w_length - 1]
            w_length = w_length - 1
        s_length = len(sentence)
    result_s = result_s[:-1]
    return result_s


def rmmcut(sentence, custom_dict, wordsdict):
    sentence = sentence.strip()
    s_length = len(sentence)
    result_s = ""
    english_word = ""
    while s_length > 0:
        # print("s_length:", s_length)
        word = sentence
        w_length = len(word)
        while w_length > 0:
            # print("    w_length:", w_length)
            if isASCIIChar(word[w_length-1]):
                # print(word[w_length-1])
                english_word = str(word[w_length-1]) + english_word
                sentence = sentence[:s_length-1]
                w_length -= 1
                s_length -= 1
                # print(english_word)
                break
            if english_word:
                # print(english_word)
                result_s = english_word + "][" + result_s
                english_word = ""
                break
            elif word in custom_dict:
                # print(word)
                result_s = word + "][" + result_s
                sentence = sentence[:s_length - w_length]
                break
            elif word in wordsdict:
                # print(word)
                result_s = word + "][" + result_s
                sentence = sentence[:s_length - w_length]
                break
            elif w_length == 1:
                # print(word)
                result_s = word + "][" + result_s
                sentence = sentence[:s_length - w_length]
                break
            else:
                word = word[1:]
            w_length = w_length - 1
        s_length = len(sentence)
    result_s = "[" + result_s[:-1] + "\n"
    return result_s


if __name__ == "__main__":
    wordsdict = gen_dict("../dict/sogou.dic_utf8")
    custom_dict = gen_custom_dict("../dict/custom.dic")

    sentence = "eip看到人资有待办但是登录系统看不到待办浏览器IE8"
    english = getASCIIWords(sentence)
    print(english)
    wordsegrmm = ''.join(fmmcut(sentence, custom_dict, wordsdict))
    print(wordsegrmm)

    desmm = open('../it_mm.txt', 'w', encoding='utf-8')
    #desrmm = open('../kf_rmm.txt', 'w', encoding='utf-8')
    with open('../IT.txt', 'r', encoding='utf-8') as src:
        for inline in src:
            wordsegfmm = ''.join(fmmcut(inline, custom_dict, wordsdict))
            wordsegrmm = ''.join(rmmcut(inline, custom_dict, wordsdict))
            desmm.write("Org:" + inline)
            desmm.write("FMM:" + wordsegfmm + "\n")
            desmm.write("RMM:" + wordsegrmm)
    desmm.close()
    #desrmm.close()
