# encoding=utf-8
# import finalseg
from .finalseg import *

sentence_list = [
    "姚晨和老凌离婚了",
    "他说的确实在理",
    "长春市长春节讲话"
]

print(u"=默认效果")

for sentence in sentence_list:
    seg_list = cut(sentence)
    print("/ ".join(seg_list))

print(u"\n=打开新词发现功能后的效果\n")

for sentence in sentence_list:
    seg_list = cut(sentence, find_new_word=True)
    print("/ ".join(seg_list))

if __name__ == "__main__":
    deshmm1 = open('question_hmm1.txt', 'w', encoding='utf-8')
    deshmm2 = open('question_hmm2.txt', 'w', encoding='utf-8')
    with open('question.txt', 'r', encoding='utf-8') as src:
        for inline in src:
            wordseghmm1 = '/'.join(cut(inline))
            wordseghmm2 = '/'.join(cut(inline, find_new_word=True))
            deshmm1.write(wordseghmm1)
            deshmm2.write(wordseghmm2)
    deshmm1.close()
    deshmm2.close()
