#!/usr/bin/env python
# coding: utf-8

# In[14]:


from chempy.util import periodic
import pandas as pd
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import plotly.express as px
plt.rcParams['figure.dpi'] = 800


# In[2]:


subreddit= "chemistry"
text = None
with open("C:/Users/Andre/Notebooks/data/{}/{}.txt".format(subreddit,subreddit), 'r',encoding='utf-8') as f:
    text = f.read()

d={}
for word in text.split(" "):
    if word in d.keys():
        d[word] = d[word]+1
    else:
        d[word]= 1
        
d


# In[3]:


names = [i.lower() for i in periodic.names]


# In[4]:


names_freq = {}
for k in names:
    if k in d.keys():
        names_freq[k] = d[k]
    else:
        names_freq[k] = 0


# In[5]:


symbol_name ={}
for i in range(118):
    symbol_name[periodic.names[i].lower()] = periodic.symbols[i]


# In[6]:


symbol_freq={}


# In[7]:


for k in symbol_name.keys():
    symbol_freq[symbol_name[k]] = names_freq[k]
    


# In[8]:


new_text = ""
for k in symbol_freq.keys():
    for i in range(symbol_freq[k]):
    
        new_text += k+" "


# In[58]:





# In[9]:


df = pd.DataFrame({"Symbol":symbol_freq.keys(),"Frequency":symbol_freq.values()})
#df.to_csv("Symbol Frequency.csv")


# In[75]:


# added row,col to csv.


# In[10]:


df=pd.read_csv("Symbol Frequency.csv")
max_freq = df.Frequency.max()
df.set_index(['Row','Column'],inplace=True)

heatmap = pd.DataFrame(columns=[i for i in range(1,19)],index=[i for i in range(1,11)])
heatmap_labels = pd.DataFrame(columns=[i for i in range(1,19)],index=[i for i in range(1,11)])

for i in heatmap.index:
    for j in heatmap.columns:
        if (i,j) in df.index:
            heatmap_labels.loc[i,j] = df.loc[(i,j), "Symbol"]
            heatmap.loc[i,j] = df.loc[(i,j), 'Frequency']/max_freq


# In[11]:


heatmap_labels.fillna("", inplace=True)


# In[13]:



fig = px.imshow(heatmap, title="Element Frequency on r/Chemistry")
fig.update_traces(text=heatmap_labels, texttemplate="%{text}")
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
fig.write_image("data/chemistry/Element Freq Norm.png")

