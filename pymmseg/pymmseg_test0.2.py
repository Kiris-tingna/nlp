# -*- coding: utf-8 -*-
from pymmseg import Analysis


def cuttest(text):
    # cut =  Analysis(text)
    wlist = [word for word in Analysis(text)]
    tmp = ""
    for w in wlist:
        tmp += w
    # print(tmp)
    # print("================================")


if __name__ == "__main__":
    descws = open('../it_mmseg.txt', 'w', encoding='utf-8')
    with open('../IT.txt', 'r', encoding='utf-8') as src:
#        sentence = src.readline().strip().lower()
#            if not sentence: break
        for sentence in src:
            print(sentence)
            # cuttest(sentence)
            mmseg = Analysis(sentence)
            for word in mmseg:
                print(word)
                descws.write(word + '\n')
    descws.close()
