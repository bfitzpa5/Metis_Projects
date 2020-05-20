# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:06:21 2020

@author: Brendan Non-Admin
"""

import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_Harry_Potter_characters'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
characters = list()

for li in soup.find_all('li'):
    text = li.text
    if re.search(r' [-–] ', text):
        characters.append([text])
        
# remove last 5 as they are not characters        
characters = characters[:-5]

def first_and_last_names(input_df):
    df = input_df.copy()
    mask = df.name.str.contains(r'the|madam', case=False)
    df.loc[:, 'first_name'] = np.where(
        mask, 
        df.name,
        df.name.str.split(' ', expand=True)[0]
    )
    df.loc[:, 'last_name'] = (df.name.str.split(' ', expand=True)
                               .iloc[:, 1:]
                               .fillna('')
                               .agg(' '.join, axis=1)
                              )
    return df

def remove_names(input_df):
    df = input_df.copy()
    # these remove duplicate first names to be safe
    characters_to_exclude = [
        'Albus Severus Potter',
        'Mary Cattermole',
        'Tom Riddle Sr.',
        'Barty Crouch Sr',
        'Lily Luna Potter',
        'James Sirius Potter',
    ]
    mask = ~df.name.isin(characters_to_exclude)
    df = df.loc[mask, ]
    return df
    
order = ['name', 'first_name', 'last_name', 'description', ]
df = (pd.DataFrame(characters, columns=['character'])
      .character.str.split(r' [-–] ', expand=True)
      .rename(columns={
          0: 'name',
          1: 'description',
          }
       )
      .pipe(remove_names)
      .pipe(first_and_last_names)
      .reindex(columns=order)
     )

# check no first names are duplicated
assert(not df.first_name.duplicated().any())

df.to_csv('characters.csv', index=False)


"""
Houses
"""
base_url = 'https://harrypotter.fandom.com/wiki/'

df = pd.read_csv('characters.csv')
df.loc[:, 'house'] = None
names = df.name.to_list()

for name in names:
    try:
        url = base_url + name.replace(' ', '_')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        house = (soup.find('div', {'data-source': 'house'})
                 .find('div', {'class': 'pi-data-value'})
                 .text
                 )
        mask = df.loc[:, 'name'] == name
        df.loc[mask, 'house'] = house
    except:
        pass
    
df.loc[:, 'house'] = (df.loc[:, 'house']
    .str.replace(r'\[\d+\]| \(likely\)| \(possibly\)', '')
)



df.to_csv('characters.csv', index=False)