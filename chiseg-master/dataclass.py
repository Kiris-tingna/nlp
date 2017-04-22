import math
import string
from .filter import *
class Chunk:
    seg = None
    seg_length = 0
    avg_word_length = 0
    word_length_variance = 0
    morh_free_degree = 0
    def __init__(self, seg):
        self.seg = seg
        self.get_seg_length()
        self.get_avg_word_length()
        self.get_variance()
        self.get_degree_free_morph()

    def get_seg_length(self):
        seg_length = 0
        for val in self.seg:
            seg_length += len(val)
        self.seg_length = seg_length

    def get_variance(self):
        valid_word_amount = 0;
        divided = 0
        for val in self.seg:
            if val != '':
                divided += (self.avg_word_length - len(val))**2
                valid_word_amount += 1
        self.word_length_variance = round(divided*1.0 / valid_word_amount,2)   

    def get_avg_word_length(self):
        valid_word_amount = 0;
        for val in self.seg:
            if val != '':
                valid_word_amount += 1  
        self.avg_word_length = round(self.seg_length * 1.0 / valid_word_amount, 2)
    
    def get_degree_free_morph(self):
        global dict_char_freq
        for val in self.seg:
            if len(val) == 1 and filter.dict_char_freq.has_key(val):
                self.morh_free_degree += math.log(string.atoi(filter.dict_char_freq[val]))