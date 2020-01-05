# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 13:19:22 2020

@author: Brendan Non-Admin
"""

import json

def story_check(kickstarter_data):
    return [x for x in kickstarter_data if x['story'] is None]

fname = r'Data/kickstarter_data.json'

with open(fname) as f:
    kickstarter_data = json.load(f)

len(story_check(kickstarter_data))


len(kickstarter_data)

fname = os.path.join(
    'Data',
    'kickstarter_data.json'
)
urls = pd.read_json(fname, 'records')
mask = urls.goal_and_pledged_backers == ''
cols = ['url']
urls = urls.loc[mask, cols]