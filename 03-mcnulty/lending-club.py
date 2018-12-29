import os
import pandas as pd
import numpy as np
import datetime as dt

os.listdir('data')

data_dict = pd.read_excel('data/LCDataDictionary.xlsx')

df = pd.read_csv('data/loan.csv')

df.shape

df.columns

df.date.unique()
