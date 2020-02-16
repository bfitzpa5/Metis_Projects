# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 11:34:36 2020

@author: Brendan Non-Admin
"""

import json
from textblob import TextBlob as tb


def main():
    with open('house_traits.json', 'r') as f:
        house_traits = json.load(f)
    
    stop_words = [
        'acting',
        'carriage',
        'charge',
        'own',
        'stab',
        'prefect',
        'pattern',
        'possible',
        'return',
        'share',
        'such',
        'tendency',
        'due',
        'selection',
        'student',
        'Many',
        'such',
        'Order',
        'house',
        'main',
        'many',
        'other',
        'point',
        'pointless',
        'regard',
    ]
    house_words = {}
    for house, traits in house_traits.items():
        blob = tb(traits)
        words = extract_nouns_and_adjs(blob, stop_words)
        house_words[house] = words
    house_words
    
    with open(r'Data\house_words.json', 'w') as f:
        json.dump(house_words, f)

def extract_nouns_and_adjs(blob, stop_words):
    blob_filtered = list(filter(lambda x: x[1] in ['JJ', 'NN'], blob.tags))
    words = sorted(list(set(map(lambda x: x[0], blob_filtered))))
    words_filtered = list(filter(lambda x: x not in stop_words, words))
    return words_filtered

if __name__ == '__main__':
    main()