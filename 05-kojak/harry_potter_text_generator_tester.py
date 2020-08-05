# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:50:53 2020

@author: Brendan Non-Admin
"""

import spacy
import kojak_utils as utils
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
from pickle import load
from numpy import random

with open('hp_textgen_tokenizer.pkl', 'rb') as f:
    tokenizer = load(f)

model = load_model('hp_textgen.h5')

book_text = utils.read_book_texts()
nlp = spacy.load('en',disable=['parser', 'tagger','ner'])
tokens = utils.separate_punc(nlp(book_text))


f = open('hp_tokenizer_model_tests.txt', 'w')

seq_len = 30
num_gen_words = 100

random.seed(11)
randos = random.randint(0, len(tokens)-seq_len, 10)
for rando in randos:
    seed_text = ' '.join(tokens[rando: rando+seq_len])
    
    f.write(seed_text + '\n')
    f.write('='*160 + '\n')
    
    args = [model, tokenizer, seq_len, seed_text, num_gen_words]
    generated_text = utils.generate_text(*args)
    
    generated_text_tokens = generated_text.split(' ')
    
    i = seq_len
    while i < len(generated_text_tokens):
        f.write(' '.join(generated_text_tokens[i-seq_len:i]))
        f.write('\n')
        i = i + seq_len
    
    f.write('\n\n\n')

f.close()