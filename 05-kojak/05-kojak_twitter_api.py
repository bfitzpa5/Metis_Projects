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

base_url = 'https://api.twitter.com/'

def authenticate():
    key_secret = '{}:{}'.format(tc['api_key'], tc['api_secret_key']).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    auth_url = '{}oauth2/token'.format(base_url)
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

def tweet_df(term, access_token):
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    search_params = {
        'q': term,
        'lang': 'en',
        #'result_type': 'popular',
    }
    search_url = '{}1.1/search/tweets.json'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    
    data = json.loads(search_resp.content)
    df = pd.DataFrame(data['statuses'])
    
    return df


def main():
    access_token = authenticate()
    
    houses = ['gryffindor', 'slytherin', 'hufflepuff', 'ravenclaw']
    frames = list()
    for house in houses:
        df = tweet_df(house, access_token)
        df.loc[:, 'house'] = house
        frames.append(df)
        
    df = pd.concat(frames, sort=False)
    df = df.set_index(df.house + '_' + df.id_str)
    
    fout = os.path.join(
        'data',
        'house_tweets.json'   
    )
    df.to_json(fout, orient='records')
    
if __name__ == '__main__':
    main()
