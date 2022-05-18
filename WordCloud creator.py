#!/usr/bin/env python
# coding: utf-8

# In[5]:


subreddit= "coronavirus"
text = None
with open("C:/Users/Andre/Notebooks/data/{}/{}.txt".format(subreddit,subreddit), 'r',encoding='utf-8') as f:
    text = f.read()


# In[3]:


import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


# In[7]:


words = []
with open("common_words.txt",'r') as f:
    words = f.readlines()

for w in words:
    i = words.index(w)
    words[i] = w.replace("\n", '')

stopwords = set(STOPWORDS)
stopwords.update(e for e in words)
stopwords.update(['got','say','go','new'])

img = Image.open('data/{}/{}.png'.format(subreddit,subreddit))
#img.resize((1000,1000))
mask = np.array(img)
wordcloud_nk = WordCloud(stopwords=stopwords, background_color=None,mode='RGBA',max_words=2000,mask=mask, max_font_size=120,collocations=False).generate(text)
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[10,10])


plt.imshow(wordcloud_nk.recolor(color_func=image_colors),interpolation='bilinear')
plt.axis('off')
plt.savefig('data/{}/{}_wc.png'.format(subreddit,subreddit), format='png')

plt.show()

