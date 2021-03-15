#Pull days price info. Pulls once a day after market close

from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import numpy as np
import json
import requests

stock_df = pd.read_csv("stocks.csv")
ticker_list = list(stock_df["Symbol"])
name_list = list(stock_df["Name"])


def get_data(ticker):
    try:
            global stock_data
            stock_data = data.DataReader(ticker,
            'yahoo',
            '2020-12-01',     #Update these params just to pull the most recent day
            '2021-3-04')
            
            stock_data['ticker'] = ticker
#             print(stock_data)
        
            return stock_data
        
    except RemoteDataError:
            print(f'no data found for {ticker}')
            

def pull_market(ticker_list):
    global market_df
    market_df = {}
    market_df = market_df = pd.DataFrame(market_df)
    
    
    for i in range(len(ticker_list)):
        
        try:
            get_data(ticker_list[i])
            market_df = market_df.append(stock_data)
            print(f"processed: {ticker_list[i]}")
        except:
            pass
    return market_df


# High	Low	Open	Close	Volume	Adj Close ticker
def load_yahoo_data_to_mongo(market_df):
    for i in range(len(market_df)):
        try:
#             print(len(reddit_response))
            document = {"Date":market_df.iloc[i]["Date"], 
                    "Low":market_df.iloc[i]["Low"], 
                    "Open":market_df.iloc[i]["Open"], 
                    "Close":market_df.iloc[i]["Close"],
                    "Volume":market_df.iloc[i]["Volume"], 
                    "Adj Close":market_df.iloc[i]["Adj Close"], 
                    "ticker":market_df.iloc[i]["ticker"]}
            stock_KPI_collection.insert_one(document)
#             print(f"wrote {i} of {len(market_df)} to mongo")
            
        except:
            print(f"generating doc {i} failed")


if __name__ == "__main__":
    pull_market(ticker_list)
    load_yahoo_data_to_mongo(market_df)
