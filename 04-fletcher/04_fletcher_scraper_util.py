# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 13:19:22 2020

@author: Brendan Non-Admin
"""

import json

def story_check(kickstarter_data):
    return [x for x in kickstarter_data if x['story'] is None]

def goal_check(kickstarter_data):
    return [x for x in kickstarter_data if x['goal_and_pledged_backers'] is None]

fname = r'Data/kickstarter_data.json'

with open(fname) as f:
    kickstarter_data = json.load(f)

len(story_check(kickstarter_data))
len(goal_check(kickstarter_data))

for i, data in enumerate(kickstarter_data[50:100]):
    print('Page {:,d}'.format(i), '\n', data['goal_and_pledged_backers'])

len(kickstarter_data)