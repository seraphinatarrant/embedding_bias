#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 02:55:14 2020

@author: s1983961
"""

import pandas as pd


path = "../data/hateval2019/"
files = "hateval2019_clean_es_"

for i in ["train","dev","test"]:
    df = pd.read_csv(path+files+i+".csv")
    
    task1 = df[["id","text","HS"]]
    task1.columns = ["id","text","label"]
    task1.to_csv(path+"task1_es_"+i+".csv")
    print(task1.label.unique())
    
    task2 = df[["id","text","TR","AG"]].loc[df["HS"]==1]
    task2["label"] = 0
    task2["label"].loc[(task2.TR == 0) & (task2.AG == 1)] = 1
    task2["label"].loc[(task2.TR == 1) & (task2.AG == 0)] = 2
    task2["label"].loc[(task2.TR == 1) & (task2.AG == 1)] = 3
    print(task2.label.unique())
    task2 = task2.drop(["TR","AG"],axis=1)
    task2.to_csv(path+"task2_es_"+i+".csv")