# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:segmenttree.py
# @time:2017/5/24 0024 16:25

from segmenttree import SegmentTree
segtree = SegmentTree(1, 8)
segtree.add(1, 3, 1)
segtree.add(3, 4, 1)
segtree.add(4, 5, 1)
segtree.add(3, 6, 2)
segtree.add(1, 71)
print(segtree.query_max(2, 5)) #This should print 5
print(segtree.query_len(2, 5)) #This should print 4
print(segtree.query_sum(2, 5)) #This should print 16

segtree = SegmentTree(0, 8)
segtree.add(1, 1, 1)
segtree.add(8, 8, 1)
print(segtree.query_max(0, 8)) #1
print(segtree.query_len(0, 8)) #2
print(segtree.query_sum(0, 8)) #2