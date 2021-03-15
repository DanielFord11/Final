#set to run every 14 min

from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import json
import requests

end_epoch = int(datetime.today().timestamp())
start_epoch = end_epoch - 840
api = PushshiftAPI()

sub_list = ['wallstreetbets', 'WallstreetbetsELITE', 'Wallstreetbets']

stock_df = pd.read_csv("stocks.csv")

ticker_list = list(stock_df["Symbol"])
name_list = list(stock_df["Name"])


#mongo dependencies
import pymongo
client = pymongo.MongoClient()
db = client["Clout_Chaser"]
collection=db["stocks"]

def scrape_reddit():
    for sub in sub_list:
        start_epoch=int(dt.datetime(2021, 2, day+1).timestamp())
        end_epoch=int(dt.datetime(2021, 2, day+2).timestamp())
        print(start_epoch)
        try:
            reddit_response = list(api.search_submissions(after=start_epoch,
                                   before=end_epoch,
                                   subreddit=sub,
                                   filter=['url','author','title','subreddit',
                                           'upvote_ratio','score'],
                                   limit=5000))
            print(f"response len:{len(reddit_response)}")
        except:
            print(f"call failed for day:{day}")
        
        for post in range(len(reddit_response)):
            try:
    #             print(len(reddit_response))
                document = {"author":reddit_response[post][0], 
                        "created": reddit_response[post][1], 
                        "score":reddit_response[post][2],
                        "subreddit":reddit_response[post][3],
                        "title":reddit_response[post][4]}
                collection.insert_one(document)
                print(f"wrote {post} of {len(reddit_response)} to mongo")
                
            except:
                print("generating doc failed")

        return

if __name__ == "__main__":
    scrape_reddit()
