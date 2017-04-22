# coding=utf-8
from .dataclass import *
import codecs
import math
import string
dict_char_freq = {}
def get_longest_avg_word_chunks(chunk_class_tuple):
    candidate_chunks = []
    longest_ave_world_length = 0
    for chunk in chunk_class_tuple:
        if chunk.avg_word_length > longest_ave_world_length:
            longest_ave_world_length = chunk.avg_word_length
    for chunk in chunk_class_tuple:
        if chunk.avg_word_length == longest_ave_world_length:
            candidate_chunks.append(chunk)
    return candidate_chunks

def get_smallest_variance_chunks(chunk_class_tuple):
    candidate_chunks = []
    smallest_variance = 1000
    for chunk in chunk_class_tuple:
        if chunk.word_length_variance < smallest_variance:
            smallest_variance = chunk.word_length_variance
    for chunk in chunk_class_tuple:
        if chunk.word_length_variance == smallest_variance:
            candidate_chunks.append(chunk)
    return candidate_chunks

def get_largest_free_morph_degree(chunk_class_tuple):
    candidate_chunks = []
    largest_free_morph_degre = 0
    for chunk in chunk_class_tuple:
        if chunk.morh_free_degree > largest_free_morph_degre:
           largest_free_morph_degre = chunk.morh_free_degree
    for chunk in chunk_class_tuple:
        if chunk.morh_free_degree == largest_free_morph_degre:
            candidate_chunks.append(chunk)
    return candidate_chunks    

def load_dict_char_freq(filepath):
    global dict_char_freq
    input_file = codecs.open('CHARFREQ.DAT','r','utf-8')
    dict_char_freq = {}
    for line in input_file.readlines():
        dict_char_freq[line[0:1]] = line[1:]
    input_file.close() 

def execute_filter_chain(Chunk_class_tuple):
    pass