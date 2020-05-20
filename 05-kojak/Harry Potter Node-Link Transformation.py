# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:43:01 2020

@author: Brendan Non-Admin
"""
from os import listdir
from itertools import combinations 
import pandas as pd
import json

datadir = "Data/Book CSVs/"
books = []
for filename in listdir(datadir):
    filepath = datadir + filename
    with open(filepath) as f:
        chapters = f.read().splitlines()
    books.append(chapters)

characters = pd.read_csv('characters.csv')

character_names = characters.first_name.to_list()
character_pairs = list(combinations(character_names, 2))

counts = {}

for character_pair in character_pairs:
    counts[character_pair] = 0
    for book in books:
        for chapter in chapters:
            if character_pair[0] in chapter and character_pair[1] in chapter:
                counts[character_pair] = counts[character_pair] + 1
            
# filter zeros
counts = {k: v for (k, v) in counts.items() if v != 0 }

def full_name_from_first_name(first_name):
    mask = characters.first_name == first_name

    full_name = characters.loc[mask, 'name'].values[0]
    return full_name

# refactor dictionar
links = []
for k, v in counts.items():
    row = {}
    source = full_name_from_first_name(k[0])
    target = full_name_from_first_name(k[1])
    value = v
    
    row['source'] = source
    row['target'] = target
    row['value'] = value
    links.append(row)

nodes = (df.loc[:, ['name', 'house']]
    .fillna('Non-Affiliated')
    .to_dict(orient='records')
)

data = {'nodes': nodes, 'links': links}

with open('harry_potter.json', 'w') as f:
    json.dump(data, f)