# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:43:01 2020

@author: Brendan Non-Admin
"""

datadir = "Data/Book CSVs/"
filename = datadir + 'philosophers_stone.txt'

with open(filename) as f:
    lines = f.read().splitlines()
    
print(lines[0][:500] + '...')