#Consolodates the Breakout Indicator Scores

import pandas as pd
import pymongo
import json
import requests


#need function to pull MarketDF from either mongo or csv


def pull_reddit_scores(df): 
    score_list = []
    for i in range(len(df)):
        global r_df
        r_df = df
        phrase = r_df.iloc[i]['ticker']
        day_start = r_df.iloc[i]['Date']
        start_stamp = datetime.timestamp(day_start)
        end_stamp = start_stamp + 86400
        doc_list = [doc for doc in collection.find( {"$and": [{"$text": { "$search": phrase }}, { "created": { "$gte": start_stamp, "$lt":end_stamp } }]} )]
        score_list.append(len(doc_list))
    r_df['reddit_scores'] = score_list
    
    return r_df


def pull_sent_scores(df): 
    score_list = []
    for i in range(len(df)):
        global fin_df
        fin_df = df
        ticker = fin_df.iloc[i]['ticker']
        convert_day = str(fin_df.iloc[i]['Date'])
        day = convert_day[0:10]
        
        try:
            sent = [doc for doc in stock_sentiment_col.find({"ticker": ticker})]
            score_list.append(sent[0][day])
            print(f"{ticker} processed")
        except:
            print(f"{ticker} failed")
            score_list.append(0)
            
    fin_df['sent_scores'] = score_list
    
    return fin_df


#need function to composite load scores to Mongo


if __name__ == "__main__":

