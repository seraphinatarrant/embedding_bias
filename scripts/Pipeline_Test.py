#!/usr/bin/env python
# coding: utf-8

# # Pipeline Test
# 
# This is a test for running the pipeline

# In[1]:


from importlib import reload
import embeddings.generate_embedding as embedding


# In[2]:


embedding = reload(embedding)

ft = embedding.train_fasttext


# In[ ]:


model = ft("../data/archive/2019_03/tweets_processed.tsv")


# In[ ]:


print(model)
model.save("../data/embeddings/model")

