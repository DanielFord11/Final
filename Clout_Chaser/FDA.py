
import pandas as pd
import pymongo
import json
import requests
import pymongo
client = pymongo.MongoClient()
db = client["Clout_Chaser"]
Stock_BI=db["Stock_BI"]


def call_FDA():

    #Create start and end variables based on job cadence
    query_url = f'https://api.fda.gov/device/pma.json?search=[{start}+TO+{end}]&limit=1000'
    response = requests.get(query_url).json()

    for i in range(len(response['results'])):

        name = response['results'][i]['applicant']
        approval = response['results'][i]['decision_code']
        decision_date = response['results'][i]['decision_date']
        
        if name in name_list and approval == 'APPR':
        
            Stock_BI.update_one({"ticker":ticker}, {"created":decision_date},
                    {'$set': {'FDA_Approval': 'APPR'}})
            
        else:
            print(f'***no ticker for: {name}***')


if __name__ == "__main__":
    call_FDA()
    
