# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 07:53:02 2020
@author: Brendan Non-Admin
"""

import os
import pandas as pd
import requests
import base64
import json
from twitter_config import tc
import datetime as dt

_base_url = 'https://api.twitter.com/'

def authenticate():
    key_secret = '{}:{}'.format(tc['api_key'], tc['api_secret_key']).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    auth_url = '{}oauth2/token'.format(_base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()['access_token']
    return access_token

def tweet_df(term, access_token, next_id=None):
    request_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    request_params = {
        'query': house,
        #'count': 200,
    }
    if next_id:
        request_params['next'] = next_id

    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/nlpanalysis.json'
    response = requests.get(url, headers=request_headers, params=request_params)

    json_data = response.json()
    df = pd.DataFrame(json_data['results'])
    
    response_next_id = json_data['next']
    
    return df, response_next_id 


def main():
    access_token = authenticate()
    
    houses = ['gryffindor', 'slytherin', 'hufflepuff', 'ravenclaw']
    frames = list()
    for house in houses:
        next_id = None
        while True:
            df, next_id = tweet_df(house, access_token, next_id)
            df.loc[:, 'house'] = house
            frames.append(df)
            if next_id is None:
                break
    
    df = pd.concat(frames, sort=False)
    df = df.set_index(df.house + '_' + df.id_str)
    df.shape
    ts = dt.datetime.now().strftime('%y%m%d')
    fout = os.path.join(
        'data',
        f"HouseTweets_{ts}.json"
    )
    df.to_json(fout, orient='records')
    print(f"\nSuccess!\nSee file located at:\t{fout}")
    
if __name__ == '__main__':
    main()
