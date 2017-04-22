# coding=utf-8

from .mmsegdict import *
from .dataclass import *
from .maxmatch import *
from test import *
from .filter import *

s = []
s.append(u'研究生命起源')
s.append(u'然后来世博园')
s.append(u'长春市长春药店')
s.append(u'主要是因为')
for sentence in s:
    print('the source sentence is',sentence)
    print('test forward_max_match')
    temp = forward_max_match(dictionary, sentence)
    stri = ''
    for i in temp:
        stri += i+'/'
    print(stri)
    print('test complex_max_match')
    temp = complex_max_match(dictionary, 'CHARFREQ.DAT',sentence)

    def print_chunk(list, i):
        for akey in list.keys():
            print(i,akey)
            temp = list.get(akey)
            if type(temp) is dict:
                print_chunk(temp,i+1)
    stri = ''
    #print_chunk(temp, 1)
    for i in temp:
        stri += i+'/'
    print(stri)
    #print 'here',temp
temp = recurse_match(dictionary, s[1], 3)

print('test chunk_tree_convert_to_chunk_tuple')
temp = chunk_tree_convert_to_chunk_tuple(temp)
for i in temp:
    for j in i:
        print(j)
    print('------------------------------')

print('test chunk_tuple_convert_Chunk_class_tuples')
temp = chunk_tuple_convert_Chunk_class_tuple(temp)
for val in temp:
    print(val.seg, val.seg_length,val.avg_word_length,val.word_length_variance)

print('test get_candidate_chunks')
temp = get_candidate_chunks(temp)
for val in temp:
    print(val.seg, val.seg_length)

print('test get_first_word_in_longest_chunk')
if get_first_word_in_longest_chunk(temp) is not None:
    print(temp[0].seg[0],val.avg_word_length)
    exit()
else:
    print('None')

print('test get_longest_avg_word_chunks')
temp = get_longest_avg_word_chunks(temp)
for val in temp:
    print(val.seg, val.avg_word_length,val.word_length_variance)

print('test get_smallest_variance_chunks')
temp = get_smallest_variance_chunks(temp)

for val in temp:
    print(val.seg, val.word_length_variance,val.morh_free_degree)

print('test get_largest_free_morph_degree')
temp = get_largest_free_morph_degree(temp)

for val in temp:
    print(val.seg, val.word_length_variance, val.morh_free_degree)

print('test get_first_word_in_longest_chunk')
if get_first_word_in_longest_chunk(temp) is not None:
    print(temp[0].seg[0])
else:
    print('None')
