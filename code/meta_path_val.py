#!/usr/bin/env python
# coding=utf-8

import random
from copy import deepcopy
import numpy as np
import io
import os
from sklearn import metrics
import tensorflow as tf
import copy
import sys

# add an element to 2-array dictionary
def addtodict2(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a: {key_b: val}})


data_query = {}
data_title = {}
threshold = 0.5
query_nei = {}
title_nei = {}
input_data='./new_eval'
output_data='./eval_nei_4order.tsv'

with io.open(input_data, 'r', encoding='utf-8') as f:
    for i, line1 in enumerate(f):
        line = line1.strip().split('\t')
        query = line[0]
        title = line[1]
        score = float(line[2])
        if len(title) == 0:
            print("title none is: ", i)
        if score >= threshold:
            addtodict2(data_query, query, title, score)
            addtodict2(data_title, title, query, score)
print("Finished: reading file as a dict.")

null_q = 0
for query in data_query:    ##for key in a和 for key in a.keys():完全等价,但是前者效率更高
    neighbor = sorted(data_query[query].items(), key=lambda item:item[1], reverse=True) ##对data_query进行排序
    nei_num = len(neighbor)
    if nei_num == 0:
        null_q += 1
        query_nei.setdefault(query, [])
    elif nei_num == 1:
        query_nei.setdefault(query, []).extend([neighbor[0][0]])
    else:
        query_nei.setdefault(query, []).extend([neighbor[0][0], neighbor[1][0]])
print("total query 's num is: ", len(data_query))
print("null query 's num is: ", null_q)

null_t = 0
for title in data_title:
    neighbor = sorted(data_title[title].items(), key=lambda item:item[1], reverse=True)
    nei_num = len(neighbor)
    if nei_num == 0:
        null_t += 1
        title_nei.setdefault(title, [])
    elif nei_num == 1:
        title_nei.setdefault(title, []).extend([neighbor[0][0]])
    else:
        title_nei.setdefault(title, []).extend([neighbor[0][0], neighbor[1][0]])
print("total title 's num is: ", len(data_title))
print("null title 's num is: ", null_t)
print("Finished: find (two) neighbors.")

with io.open(input_data, 'r', encoding='utf-8') as fa, io.open(output_data, 'w', encoding='utf-8') as fb:
    for i, line1 in enumerate(fa):
        line = line1.strip().split('\t')
        query = line[0]
        title = line[1]
        score = line[2]
        qiqiq1_t1, qiqiq1_q2, qiqiq2_t3, qiqiq2_q4 = title, query, title, query
        qiqiq1_t5, qiqiq1_q6, qiqiq2_t7, qiqiq2_q8 = title, query, title, query
        iqiqi1_q1, iqiqi1_t2, iqiqi2_q3, iqiqi2_t4 = query, title, query, title
        iqiqi1_q5, iqiqi1_t6, iqiqi2_q7, iqiqi2_t8 = query, title, query, title
        if query in query_nei:
            qiqiq1_t1 = query_nei[query][0]
            if qiqiq1_t1 in title_nei:
                qiqiq1_q2 = title_nei[qiqiq1_t1][0]
                if qiqiq1_q2 in query_nei:
                    qiqiq2_t3 = query_nei[qiqiq1_q2][0]
                    if qiqiq2_t3 in title_nei:
                        qiqiq2_q4 = title_nei[qiqiq2_t3][0]
                        if len(title_nei[qiqiq2_t3]) > 1:
                            qiqiq1_t5 = qiqiq1_t1
                            qiqiq1_q6 = qiqiq1_q2
                            qiqiq2_t7 = qiqiq2_t3
                            qiqiq2_q8 = title_nei[qiqiq2_t3][1]
        if title in title_nei:
            iqiqi1_q1 = title_nei[title][0]
            if iqiqi1_q1 in query_nei:
                iqiqi1_t2 = query_nei[iqiqi1_q1][0]
                if iqiqi1_t2 in title_nei:
                    iqiqi2_q3 = title_nei[iqiqi1_t2][0]
                    if iqiqi2_q3 in query_nei:
                        iqiqi2_t4 = query_nei[iqiqi2_q3][0]
                        if len(query_nei[iqiqi2_q3]) > 1:
                            iqiqi1_q5 = iqiqi1_q1
                            iqiqi1_t6 = iqiqi1_t2
                            iqiqi2_q7 = iqiqi2_q3
                            iqiqi2_t8 = query_nei[iqiqi2_q3][1]

        fb.write(query + '\t' + title + '\t' + score + '\t')
        fb.write(qiqiq1_t1 + '\t' + qiqiq1_q2 + '\t' + qiqiq2_t3 + '\t' + qiqiq2_q4 + '\t')
        fb.write(qiqiq1_t5 + '\t' + qiqiq1_q6 + '\t' + qiqiq2_t7 + '\t' + qiqiq2_q8 + '\t')
        fb.write(iqiqi1_q1 + '\t' + iqiqi1_t2 + '\t' + iqiqi2_q3 + '\t' + iqiqi2_t4 + '\t')
        fb.write(iqiqi1_q5 + '\t' + iqiqi1_t6 + '\t' + iqiqi2_q7 + '\t' + iqiqi2_t8 + '\n')
print("Finished!")




