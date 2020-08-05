# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:13:20 2020

@author: Brendan Non-Admin
"""

import os
import time
import unicodedata
import spacy
import numpy as np
import kojak_utils as utils
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
import datetime as dt

datapath = os.path.join('Data', 'Book TXTs')

os.listdir(datapath)

book_filenames = [
    'philosophers_stone.txt',
    'chamber_of_secrets.txt',
    'prisoner_of_azkaban.txt',
    'goblet_of_fire.txt',
    'order_of_the_phoenix.txt',
    'half_blood_prince.txt',
    'deathly_hallows.txt',
]

book_filename = book_filenames[0]

filepath = os.path.join(datapath, book_filename)
    
with open(filepath, 'r') as f:
    book_text = unicodedata.normalize("NFKD", f.read())

nlp = spacy.load('en',disable=['parser', 'tagger','ner'])

tokens = utils.separate_punc(nlp(book_text))

# organize into sequences of tokens
train_len = 30 + 1

text_sequences = utils.create_text_sequences(tokens, train_len)

' '.join(text_sequences[0])
len(text_sequences)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_sequences)
sequences = np.array(tokenizer.texts_to_sequences(text_sequences))

print(sequences[0].tolist())

for i in sequences[0]:
    print(f'{i:>5,.0f}: {tokenizer.index_word[i]:<50}')

vocabulary_size = len(tokenizer.word_counts)

X = sequences[:,:-1]
y = to_categorical(sequences[:,-1], num_classes=vocabulary_size+1)

seq_len = X.shape[1]

model = utils.initalize_model(vocabulary_size+1, seq_len)

start = time.time()
start_str = utils.time_to_iso(start)
print(f"Started at:  {start_str:>15}")
model.fit(X, y, batch_size=128, epochs=300, verbose=1)
end = time.time()
end_str = utils.time_to_iso(end)
print(f"Ended at:    {end_str:>15}")
duration = end - start
duration = 4 * 60**2 + 2 * 60**1 + 58 * 60**0
duration_factored = utils.seconds_factorization(duration)
print("Duration:    {} days, {} hours, {} minutes, and {} seconds"
      .format(*duration_factored))