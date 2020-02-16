# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 11:34:36 2020

@author: Brendan Non-Admin
"""

import json
from textblob import TextBlob as tb

gryffindor = "The Gryffindor house emphasises the traits of courage as well as \"daring, nerve, and chivalry,\" and thus its members are generally regarded as brave, though sometimes to the point of recklessness. Some Gryffindors have also been noted to be short-tempered. Notably, Gryffindor house contributed many members to Dumbledore's Army and the Order of the Phoenix, although this may have been because the main members made it a point not to associate with other houses. According to Phineas Nigellus Black, members of other houses, particularly Slytherin, sometimes feel that Gryffindors engage in \"pointless heroics.\" Another Slytherin, Severus Snape, considered many Gryffindors to be self-righteous and arrogant, with no regard for rule"

t = tb(gryffindor)

t_filtered = list(filter(lambda x: x[1] in ['JJ', 'NN'], t.tags))

words = sorted(list(set(map(lambda x: x[0], t_filtered))))

stop_words = [
    'Order',
    'house',
    'main',
    'many',
    'other',
    'point',
    'pointless',
    'regard',
]
words_filtered = list(filter(lambda x: x not in stop_words, words))

house_dict = {}
house_dict['gryffindor'] = words_filtered

fname = r'Data\house_words.json'
with open(fname, 'w') as f:
    json.dump(house_dict, f)