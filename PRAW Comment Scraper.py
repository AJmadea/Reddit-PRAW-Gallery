#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
from datetime import datetime
from os.path import exists
import os


# In[33]:


import praw

import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

user_id = "nzfjg2VrHoX2n8xwLhnrGA"
secret = "GC1fkuD6TwYZGFX5YCtnkLYSTaa_-w"

reddit = praw.Reddit(
    client_id=user_id,
    client_secret=secret,
    user_agent="TeaJeascy",
)

reddit.read_only


# In[1]:


import re
def clean_up(words):
    words = words.lower()
    new_list = []
    for word in words.split(' '):
        new_list.append( re.sub(r'\W+', '', word))
    return new_list


# In[38]:



srs =["AskReddit"]

for s in srs:
    data_words=""

    for submission in reddit.subreddit(s).top(limit=1_000_000):
        print(submission.title)
        for top_level_comment in submission.comments:
            try:
                for words in clean_up(top_level_comment.body):
                    #print(data_words)
                    data_words+="{} ".format(words)

            except AttributeError as err:
                continue

    _dir = "data/{}".format(s)
    if not exists(_dir):
        os.mkdir(_dir)
        
    with open("data/{}/{}.txt".format(s,s), 'w', encoding='utf-8') as f:
        f.write(data_words)
            
    words = []
    with open("common_words.txt",'r') as f:
        words = f.readlines()

    for w in words:
        i = words.index(w)
        words[i] = w.replace("\n", '')

    stopwords = set(STOPWORDS)
    stopwords.update(e for e in words)
    stopwords.update(['got','say','go','new','retard','retarded'])

    wordcloud_nk = WordCloud(stopwords=stopwords, background_color=None,mode='RGBA',max_words=1000, max_font_size=120,collocations=False).generate(data_words)
    
    plt.figure(figsize=[7,7])

    plt.imshow(wordcloud_nk)
    plt.axis('off')
    plt.savefig(_dir+'/{}_wc.png'.format(s), format='png')

