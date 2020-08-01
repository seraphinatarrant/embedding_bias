#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 01:27:08 2020

@author: s1983961
"""


import numpy as np
import codecs


fname = "../../glove-twitter-100.txt"

print("Loading pretrained word vectors from", fname)
    
word_vecs = {}

f = codecs.open(fname, 'r', encoding="utf8")
f.readline()

flag = 0
item = []

for line in f:
    line = line.split(" ", 1)
    if len(line) == 1:
        item.append(line)
        flag = 1
        continue
    
    if flag == 1:
        item.append([line[0]])
        flag = 0
    
    key = line[0].lower()
    word_vecs[key] = np.fromstring(line[1], dtype="float64", sep=" ")
    
    
for i in item:
    print(i)

print(len(word_vecs), "vectors loaded from", fname)