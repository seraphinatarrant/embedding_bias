#!/usr/bin/env python
# coding: utf-8

# # Clean HatEval
# 
# This is a script to clean the HatEval dataset and to separate it into the two different tasks that we will be using it for. I'm assuming that it is saved to ``data/hateval2019``.

# In[ ]:


import pandas as pd


# We establish the path to our data and the generic name that our preprocessed datasets have.

# In[ ]:


path = "../data/hateval2019/"
files = "hateval2019_clean_es_"


# The first task is hate speech detection, so we only keep the HS label from the dataset.

# In[ ]:


for i in ["train","dev","test"]:
    df = pd.read_csv(path+files+i+".csv")
    
    task = df[["id","text","HS"]]
    task.columns = ["id","text","label"]
    task.to_csv(path+"task1_es_"+i+".csv")
    
    if i != "test":
        task.to_csv(path+"task1_g1_"+i+".csv")
        task.to_csv(path+"task1_g2_"+i+".csv")
        
    else:
        ln = df.shape[0] // 2
        group1 = task.iloc[:ln]
        group1.to_csv(path+"task1_g1_"+i+".csv")
        group2 = task.iloc[ln:]
        group2.to_csv(path+"task1_g2_"+i+".csv")


# The second task requires us to consider hate Tweets. Here we have to determine whether they are targeted or not and if they are agressive or not. We decided to make this task a multilabel classification task instead of a multiclass one, so we set the following labels:
# 1. Neither targeted nor agressive
# 1. Agressive but not targeted
# 1. Targeted but not agressive
# 1. Targeted and agressive

# In[ ]:


for i in ["train","dev"]:
    df = pd.read_csv(path+files+i+".csv")
    
    task = df
    task.to_csv(path+"task2_es_"+i+".csv")
    task.to_csv(path+"task2_g1_"+i+".csv")
    task.to_csv(path+"task2_g2_"+i+".csv")
        
    
for i in ["test"]:
    df = pd.read_csv(path+files+i+".csv")
    ln = df.shape[0] // 2
    df_g1 = df[:ln]
    df_g2 = df[ln:]
    
    for data, name in [(df,"es") , (df_g1,"g1"), (df_g2,"g2")]:
    
        task = data.loc[data["HS"]==1]
        task.to_csv(path+"task2_"+name+"_"+i+".csv")

