# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:mmseg1.py
# @time:2017/6/26 0026 11:11
#coding:utf-8
from collections import defaultdict
import codecs
from math import log


class Trie(object):
    class TrieNode():
        def __init__(self):
            self.value = 0
            self.trans = {}

    def __init__(self):
        self.root = self.TrieNode()

    def add(self, word, value=1):
        cur = self.root
        for ch in word:
            try:
                cur = cur.trans[ch]
            except:
                cur.trans[ch] = self.TrieNode()
                cur = cur.trans[ch]
        cur.value = value

    def _walk(self, node, ch):
        if ch in node.trans:
            node = node.trans[ch]
            return node, node.value
        else:
            return None, 0

    def match_all(self, s):
        ret = []
        cur = self.root
        for ch in s:
            cur, value = self._walk(cur, ch)
            if not cur:
                break
            if value:
                ret.append(value)
        return ret


class Dict(Trie):
    def __init__(self, filename):
        super(Dict, self).__init__()
        self.load(filename)

    def load(self, filename):
        with codecs.open(filename, "r", "utf-8") as f:
            for line in f:
                word = line.strip()
                self.add(word, word)


class CharFreq(defaultdict):
    def __init__(self, filename):
        super(CharFreq, self).__init__(lambda: 1)
        self.load(filename)

    def load(self, filename):
        with codecs.open(filename, "r", "utf-8") as f:
            for line in f:
                line = line.strip()
                word, freq = line.split(' ')
                self[word] = freq


class MMSEG():
    class Chunk():
        def __init__(self, words, chars):
            self.words = words
            self.lens = map(lambda x: len(x), words)
            self.length = sum(self.lens)
            self.average = self.length * 1.0 / len(words)
            self.variance = sum(map(lambda x: (x - self.average) ** 2, self.lens)) / len(words)
            self.free = sum(log(float(chars[w])) for w in self.words if len(w) == 1)

        def __lt__(self, other):
            return (self.length, self.average, -self.variance, self.free) < (other.length, other.average, -other.variance, other.free)

    def __init__(self, dic, chars):
        self.dic = dic
        self.chars = chars

    def __get_chunks(self, s, depth=3):
        ret = []

        def __get_chunk(self, s, num, seg):
            if not num or not s:
                if seg:
                    ret.append(self.Chunk(seg, self.chars))
                return
            else:
                m = self.dic.match_all(s)
                if not m:
                    __get_chunk(self, s[1:], num - 1, seg + [s[0]])
                else:
                    for w in m:
                        __get_chunk(self, s[len(w):], num - 1, seg + [w])
        __get_chunk(self, s, depth, [])
        return ret

    def segment(self, s):
        while s:
            chunks = self.__get_chunks(s)
            best = max(chunks)
            yield best.words[0]
            s = s[len(best.words[0]):]

if __name__ == "__main__":
    dic = Dict("words.dic")
    chars = CharFreq('chars.dic')
    mmseg = MMSEG(dic, chars)
    print (' '.join(mmseg.segment("北京欢迎你")))
    print (' '.join(mmseg.segment("研究生命起源的原因主要是因为它的重要性")))
    print (' '.join(mmseg.segment('开发票')))
    print (' '.join(mmseg.segment('武松杀嫂雕塑是艺术，还是恶俗？大家怎么看的？')))
    print (' '.join(mmseg.segment('陈明真做客《麻辣天后宫》的那期视频哪里有？')))
    print (' '.join(mmseg.segment('压缩技术是解决网络传输负担的 有效技术。数据压缩有无损压缩和有损压缩两种。在搜索引擎中用到的压缩技术属于无损压缩。接下来，我们将先讲解各种倒排索引压缩算法，然后来分析搜索引擎技术中词典和倒排表的压缩。')))