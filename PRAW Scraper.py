#!/usr/bin/env python
# coding: utf-8

# In[71]:


import pandas as pd
import time
from datetime import datetime
import praw
import json
import glob
from os.path import exists
import logging


# In[72]:


def get_data(subreddit,n,types,top_type=""):
    data=pd.DataFrame()
    
    if types=="top":
        assert top_type in top_parts
        submissions = reddit.subreddit(subreddit).top(top_type, limit=n)
        
    elif types=="hot":
        submissions = reddit.subreddit(subreddit).hot(limit=n)
    else:
        submissions = reddit.subreddit(subreddit).new(limit=n)
        
    for submission in submissions:
        #print(submission.title,"\n")
        data=data.append({"Datetime":datetime.fromtimestamp(submission.created_utc),
                    "Title":submission.title,
                    "UpvoteRatio":submission.upvote_ratio,
                    "Fullname":submission.name,
                    "Comments":submission.num_comments,
                    "id":submission.id,
                    "Score":submission.score,
                    "Datetime Retreived":datetime.now()},ignore_index=True)
    data['Subreddit']=subreddit
    data["Type"]=types
    
    if types=="top":
        data["Type"] = types + "-"+top_type
    
    return data

if __name__ == "__main__":
    try:
        if not exists('logs'):
            os.mkdir('logs')

        logging.basicConfig(filename="logs/runtime {}.log".format(datetime.now().strftime("%Y%m%d %H%M%S")), 
                            encoding='utf-8', level=logging.INFO)
        logging.info("hi")

        try:
            with open("credentials.json", 'r') as f:
                credentials = json.load(f)
            logging.info("Credentials Loaded")
        except FileNotFoundError as err:
            logging.info("File not found :()")

        reddit = praw.Reddit(
            client_id=credentials['user_id'],
            client_secret=credentials['secret'],
            user_agent=credentials['user_agent'],
        )

        print(reddit.read_only)

        subreddits = ''

        with open('subreddits.txt','r') as f:
            subreddits = f.read()

        subreddits = subreddits.split('\n')
        logging.info("Subreddits\n{}".format(subreddits))
        print(subreddits)

        top_parts = ["hour", "day","week", "month", "year", "all"]

        frames=[]
        st = time.time()
        for subreddit in subreddits:
            print(subreddit)
            for top_p in top_parts:
                frames.append(get_data(subreddit,5000,"top", top_p))
            frames.append(get_data(subreddit,5000,"hot"))
            frames.append(get_data(subreddit,5000,"new"))

        if not exists('data'):
            os.mkdir('data')


        combined = pd.concat(frames)
        combined.drop_duplicates(inplace=True)
        print(combined.shape)
        combined.to_csv("data/Combined PRAW Data.csv", mode='a')

        et = time.time()

        logging.info("Ended data collection.")
        logging.info("Runtime: {} min".format(round((et - st)/60,2)))
    except Exception as err:
        logging.info(err)
        print(err)

