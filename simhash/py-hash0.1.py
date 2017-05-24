# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:py-hash0.1.py
# @time:2017/5/24 0024 16:31

from hashes.simhash import simhash
hash1 = simhash('This is a test string one.')
hash2 = simhash('This is a test string TWO.')
print(hash1,hash2)