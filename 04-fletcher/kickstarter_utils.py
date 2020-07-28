# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:31:16 2020

@author: Brendan Non-Admin
"""
from pandas import DataFrame
from selenium import webdriver
import json
import random

def create_df_topic_word_lists(lda, cv, df, n=10,
                               verbose=False, f=None):
    topic_word_lists = list()
    components = lda.components_
    df_value_counts = df.loc[:, 'topic_id'].value_counts()
    
    for i, topic in enumerate(components):
        topic_num = i + 1
        word_list = [cv.get_feature_names()[index] for index in topic.argsort()[-n:]]
        topic_word_lists.append(word_list)
        if verbose or f:
            count = df_value_counts[topic_num]
            header_desc = f"The TOP {n} WORDS FOR TOPIC #{topic_num} ({count} total stories)"
        if verbose:
            print(header_desc)
            print(word_list)
            print('\n\n')
        if f:
            f.write(header_desc)
            f.write('\n' + ', '.join(word_list) + '\n')
            f.write('\n\n')
    columns = ['Word {}'.format(x) for x in range(1, n+1)]
    index = ['Topic {}'.format(x) for x in range(1, len(components)+1)]
    return DataFrame(topic_word_lists, index, columns)

def show_random_pitch():
    with open(r'Data/kickstarter_data.json') as f:
        data = json.load(f)
    
    driver_file = r'C:\Users\Brendan Non-Admin\Downloads\chromedriver.exe'
    driver = webdriver.Chrome(driver_file)
    
    get_next_url = 'yes'
    
    while get_next_url == 'yes':
        get_next_url = get_next_url.lower()
        if get_next_url not in ['yes', 'no']:
            print('Input must be either "yes" or "no"')
            get_next_url = input('Get another page? Enter "yes" or "no": ')
            print()
        elif get_next_url == "yes":
            pitch_idx = random.randint(0, len(data) - 1)
            project_data = data[pitch_idx]
            project_name = project_data['project_name']            
            url = project_data['url']
            
            if project_name:
                print(f"\nLoading page for {project_name}")
            else:
                print(f"\nLoading page for {url}")
            
            driver.get(url)
            
            get_next_url = input('Get another page? Enter "yes" or "no": ')
    
    driver.quit()
    
show_random_pitch()