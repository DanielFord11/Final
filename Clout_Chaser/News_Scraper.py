#script scrapes and runs sentiment analysis from aggregated finviz headlines 
def main():
    
    from urllib.request import urlopen, Request
    from bs4 import BeautifulSoup
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import pandas as pd
    import pymongo
    import json
    import requests

    client = pymongo.MongoClient()
    stock_sentiment_col = db["stock_sentiment"]
    finviz_url = 'https://finviz.com/quote.ashx?t='
    stock_df = pd.read_csv("stocks.csv")
    ticker_list = list(stock_df["Symbol"])
    name_list = list(stock_df["Name"])
    end_epoch = int(datetime.today().timestamp())
    start_epoch = end_epoch - 840
    news_tables = {}
    
    for i in range(len(ticker_list)):
        try:
            url = finviz_url + ticker_list[i]

            req = Request(url=url, headers={'user-agent': 'my-app'})
            response = urlopen(req)

            html = BeautifulSoup(response, features='html.parser')
            news_table = html.find(id='news-table')
            news_tables[ticker_list[i]] = news_table
            
            print(f"{ticker_list[i+4000]} processed {i}")
            
        except:
            print(f"{ticker_list[i+4000]} didn't process")

    parsed_data = []

    for ticker, news_table in news_tables.items():

        try:
            for row in news_table.findAll('tr'):

                title = row.a.text
                date_data = row.td.text.split(' ')

                if len(date_data) == 1:
                    time = date_data[0]
                    parsed_data.append([ticker, date, time, title])
                else:
                    date = date_data[0]
                    time = date_data[1]
                    parsed_data.append([ticker, date, time, title])
        except:
            print(f"{ticker} failed")

    try:                                          
        df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
        vader = SentimentIntensityAnalyzer()
        f = lambda title: vader.polarity_scores(title)['compound']
        df['compound'] = df['title'].apply(f)
        df['date'] = pd.to_datetime(df.date).dt.date

        mean_df = df.groupby(['ticker', 'date']).mean().unstack()
        mean_df = mean_df.xs('compound', axis="columns")

        sentdf = mean_df.fillna(0)
    except:
        print('sentiment analysis failed')


    last = len(sentdf.columns)
    index = sentdf.columns[last-1]
    current_day = sentdf[index]
    current_day = pd.DataFrame(test)
    current_day = current_day.reset_index()

    for i in range(len(current_day)):

        try:
            sent_score = current_day.loc[i,:][current_day.columns[1]]
            ticker = current_day.loc[i,:]['ticker']
            
            stock_sentiment_col.update_one({"ticker":ticker},
                        {'$set': {index.isocalendar(): sent_score}})
        except:
            print(f'failed to write {ticker} to mongo')
            

if __name__ == "__main__":
    main()

