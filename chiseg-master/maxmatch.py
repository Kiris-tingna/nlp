# coding=utf-8
from .dataclass import *
from .filter import *

def forward_max_match(mmseg_dict, src_sentence):
    start_point = 0
    word_length = len(src_sentence)
    result = [];
    while start_point < len(src_sentence) :
        if src_sentence[start_point : start_point + word_length] in mmseg_dict or word_length == 1:
            result.append(src_sentence[start_point: start_point + word_length])
            start_point = start_point + word_length;
            word_length = len(src_sentence) - start_point
        else :
            word_length -= 1
    return result

def reverse_max_match(dict, sentence):
    pass

def simple_max_match(dict, sentent):
    pass

def complex_max_match(mmseg_dict, char_freq_dict, src_sentence):
    sentence = src_sentence
    result = []
    load_dict_char_freq(char_freq_dict)
    while len(sentence) > 0:
        chunk_tree = recurse_match(mmseg_dict, sentence, 3)
        temp = chunk_tree_convert_to_chunk_tuple(chunk_tree)
        temp = chunk_tuple_convert_Chunk_class_tuple(temp)
        temp = get_candidate_chunks(temp)
        if get_first_word_in_longest_chunk(temp) is not None:
            result.append(temp[0].seg[0])
            sentence = sentence[len(temp[0].seg[0]):len(sentence)]
        else:
            temp = get_longest_avg_word_chunks(temp)
            if get_first_word_in_longest_chunk(temp) is not None:
                result.append(temp[0].seg[0])
                sentence = sentence[len(temp[0].seg[0]):len(sentence)]
            else:
                temp = get_smallest_variance_chunks(temp)
                if get_first_word_in_longest_chunk(temp) is not None:
                    result.append(temp[0].seg[0])
                    sentence = sentence[len(temp[0].seg[0]):len(sentence)]
                else: 
                    temp = get_largest_free_morph_degree(temp)
                    if get_first_word_in_longest_chunk(temp) is not None:
                        result.append(temp[0].seg[0])
                        sentence = sentence[len(temp[0].seg[0]):len(sentence)]
                    else :
                        print 'Exception'
                        return
                    pass #执行第四条规则
        '''print '-------------'
        for val in result:
            print val
        print '-------------'
        '''
        
    return result

def recurse_match(mmseg_dict, src_sentence, i):
    chunk_tree = {}
    sentence_length = len(src_sentence)
    if sentence_length >= 1:
        word_length = 1 
    else:
        word_length = 0
    while word_length <= sentence_length:
    #while word_length <= sentence_length - i + 1 :
        if src_sentence[0:word_length] in mmseg_dict or src_sentence[0:word_length] == '':
        #if src_sentence[0:word_length] in mmseg_dict :
            chunk_tree.update({src_sentence[0:word_length]:None}) 
            if i > 1:
                chunk_tree.update({src_sentence[0:word_length]: \
                recurse_match(mmseg_dict, src_sentence[word_length : len(src_sentence)], i - 1)})
        word_length += 1
    return chunk_tree;

def chunk_tree_convert_to_chunk_tuple(chunk_tree):
    segmented_sentence = [];
    for i in chunk_tree.keys():
        for j in chunk_tree.get(i).keys():
            for k in chunk_tree.get(i).get(j).keys():
                segmented_sentence.append([i,j,k])
    return segmented_sentence

def get_candidate_chunks(chunk_class_tuple):
    candidate_chunks = []
    longest = 0
    for chunk in chunk_class_tuple:
        if chunk.seg_length > longest:
            longest = chunk.seg_length
    for chunk in chunk_class_tuple:
        if chunk.seg_length == longest:
            candidate_chunks.append(chunk)
    return candidate_chunks

def chunk_tuple_convert_Chunk_class_tuple(chunk_tuple):
    chunk_class_tuple = [];
    for val in chunk_tuple:
        chunk_class_tuple.append(Chunk(val))
    
    return chunk_class_tuple

def get_first_word_in_longest_chunk(candidate_chunks):
    candidate_chunks_amount = len(candidate_chunks)
    first_word = candidate_chunks[0].seg[0]
    if candidate_chunks_amount > 1:
        for i in range(candidate_chunks_amount):
            if  first_word != candidate_chunks[i].seg[0]:
                first_word = None
                break
    return first_word
