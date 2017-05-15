descws = open('words.dic', 'w', encoding='utf-8')
with open('dict_medium.dic', 'r', encoding='utf-8') as src:
    # sentence = src.readline().strip().split()
    for sentence in src:
        # print(sentence)
        word = sentence.strip().split()
        # print(word[0])
        descws.write(word[0] + '\n')
descws.close()
