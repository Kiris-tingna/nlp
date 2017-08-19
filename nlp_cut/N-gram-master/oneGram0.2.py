# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: kevin
@contact: liujiezhang@bupt.edu.cn
@file: oneGram.py
@time: 16/10/7 下午5:11
"""
from process import *


class Dictionary:
    '''
    Dictionary Information and mananger
    '''

    def __init__(self):

        # count train.txt words
        self.word_dict = toWordSet()

        self.N = len(self.word_dict.keys())

    def getPValue(self, word):
        '''
        计算word的频率
        :param word: 词
        :return: 频率的log值
        '''
        if not self.inDict(word):
            return 1.0 / self.N
        return self.word_dict[word] / self.N

    def inDict(self, word):
        '''
        word是否在dict中
        :param word: 词
        :return: True or False
        '''
        return word in self.word_dict

    def totalNum(self):
        return self.N

    def getDict(self):
        return self.word_dict


class DictionarySmooth:
    '''
    Dictionary Information and mananger with witten-bell smooth
    '''

    def __init__(self):

        # count train.txt words
        self.word_dict = wittenBellSmoothing(
            unknowWordsSetZero(toWordSet(), file_name='test.txt'))

        self.N = len(self.word_dict.keys())

    def getPValue(self, word):
        '''
        计算word的频率
        :param word: 词
        :return: 频率的log值
        '''
        return self.word_dict[word]

    def inDict(self, word):
        '''
        word是否在dict中
        :param word: 词
        :return: True or False
        '''
        return word in self.word_dict

    def totalNum(self):
        return self.N

    def getDict(self):
        return self.word_dict


class oneGram(DictionarySmooth):
    '''
    一元模型
    '''

    def __init__(self, split='back'):
        # 继承Dictionary类
        DictionarySmooth.__init__(self)

        self.DICT = Dictionary
        self.words = []
        self.value_dict = {}
        self.seg_dict = {}
        self.split_way = split
        self.PUNC = getPunciton()

    def backwardSplitSentence(self, sentence, word_max_len=5):
        '''
        后向切词
        :param sentence: 待切分文本
        :param word_max_len: 最大词长
        :return: 切分元组列表
        '''
        words = []
        sentence_len = len(sentence)
        range_max = [sentence_len, word_max_len][sentence_len > word_max_len]
        for i in range(range_max - 1):
            words.append((sentence[:i + 1], sentence[i + 1:]))
        return words

    def forwardSplitSentence(self, sentence, word_max_len=5):
        '''
        前向切词
        :param sentence: 待切分文本
        :param word_max_len: 最大词长
        :return: 切分元组列表
        '''
        words = []
        sentence_len = len(sentence)
        range_max = [sentence_len, word_max_len][sentence_len > word_max_len]
        for i in range(range_max - 1):
            words.append((sentence[:-(i + 1)], sentence[-(i + 1):]))
        return words

    def maxP(self, sentence):
        '''
        计算最大切分方案
        :param sentence: 待切分句子
        :return:
        '''
        # 遍历所有切分组合中，找出最大概率切分
        if len(sentence) <= 1:
            return self.DICT.getPValue(self, sentence)
        # 判断切词方向：backward 或 forward
        sentence_split_words = [self.backwardSplitSentence(
            sentence), self.forwardSplitSentence(sentence)][self.split_way != 'back']
        # 记录最大概率值
        max_p_value = 0
        # 储存最大概率下的切分组合
        word_pairs = []
        # 组合概率值
        word_p = 0

        for pair in sentence_split_words:
            p1, p2 = 0, 0

            if pair[0] in self.value_dict:
                p1 = self.value_dict[pair[0]]
            else:
                p1 = self.maxP(pair[0])

            if pair[1] in self.value_dict:
                p2 = self.value_dict[pair[1]]
            else:
                p2 = self.maxP(pair[1])

            word_p = p1 * p2

            if max_p_value < word_p:
                max_p_value = word_p
                word_pairs = pair
        # 在词典中查询当前句对应的频率，不存在时，返回 1/N
        sentence_p_value = self.DICT.getPValue(self, sentence)
        # 不切分概率最大时，更新各值
        if sentence_p_value > max_p_value and self.DICT.inDict(self, sentence):
            self.value_dict[sentence] = sentence_p_value
            self.seg_dict[sentence] = sentence
            return sentence_p_value
        # 某种切分组合概率最大时，更新sentence对应概率，避免后续切分重复计算
        else:
            self.value_dict[sentence] = max_p_value
            self.seg_dict[sentence] = word_pairs
            return max_p_value

    def getSeg(self):
        return self.seg_dict

    def segment(self, sentence):
        '''
        分词调用入口
        :param sentence: 待切分文本
        :return: 最佳切分词列表
        '''
        words = []
        sentences = []
        # 若含有标点，以标点分割
        start = -1
        for i in range(len(sentence)):
            if sentence[i] in self.PUNC and i < len(sentence):
                sentences.append(sentence[start + 1:i])
                sentences.append(sentence[i])
                start = i
        if not sentences:
            sentences.append(sentence)
        # 对每个标点分割的断句进行分词
        for sent in sentences:
            self.maxP(sent)
            words.extend(self.dumpSeg(sent))
        return words

    def dumpSeg(self, sentence):
        '''
        输出分词结果列表
        :param sentence:
        :return:
        '''
        words = []
        if sentence in self.seg_dict:
            pair = self.seg_dict[sentence]
            if isinstance(pair, tuple):
                words.extend(self.dumpSeg(pair[0]))
                words.extend(self.dumpSeg(pair[1]))
            else:
                if pair == sentence:
                    words.append(pair)
                else:
                    words.extend(self.dumpSeg(pair))
        else:
            words.append(sentence)
        return words


if __name__ == '__main__':
    OG = oneGram()
    wordseg = []
    des =  open('../question_onegram.txt', 'w', encoding='utf-8')
    with open('../question.txt', 'r', encoding='utf-8') as src:
        for inline in src:
            wordseg = OG.segment(inline)
            for word in wordseg:
                des.write(word + '/')
    des.close()
    src.close()