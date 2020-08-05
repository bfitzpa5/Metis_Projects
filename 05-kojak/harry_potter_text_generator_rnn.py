# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:13:20 2020

@author: Brendan Non-Admin
"""

import time
import spacy
import numpy as np
import kojak_utils as utils
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from pickle import dump

book_text = utils.read_book_texts()

nlp = spacy.load('en',disable=['parser', 'tagger','ner'])
# nlp.max_length = len(book_text) + 1

tokens = utils.separate_punc(nlp(book_text))

# organize into sequences of tokens
train_len = 30 + 1

text_sequences = utils.create_text_sequences(tokens, train_len)

#' '.join(text_sequences[0])
#len(text_sequences)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_sequences)
sequences = np.array(tokenizer.texts_to_sequences(text_sequences))

# print(sequences[0].tolist())

#for i in sequences[0]:
#    print(f'{i:>5,.0f}: {tokenizer.index_word[i]:<50}')

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

model.save('hp_textgen.h5')
dump(tokenizer, open('hp_textgen_tokenizer.pkl', 'wb'))
