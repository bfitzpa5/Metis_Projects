# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:50:53 2020

@author: Brendan Non-Admin
"""

import os
import spacy
import kojak_utils as utils
from keras.preprocessing.text import Tokenizer # required for the pickle load
from keras.models import load_model
from pickle import load
from numpy import random


def main():
    modelspath = os.path.join('Data', 'Models')
    filepath = os.path.join(modelspath, 'hp_textgen_tokenizer.pkl')
    with open(filepath, 'rb') as f:
        tokenizer = load(f)
    
    filepath = os.path.join(modelspath, 'hp_textgen.h5')
    model = load_model(filepath)
    
    book_text = utils.read_book_texts()
    nlp = spacy.load('en',disable=['parser', 'tagger','ner'])
    tokens = utils.separate_punc(nlp(book_text))
    
    
    filepath = os.path.join(modelspath, 'hp_tokenizer_model_tests.txt')
    f = open(filepath, 'w')
    
    seq_len = 30
    num_gen_words = 100
    
    random.seed(11)
    randos = random.randint(0, len(tokens)-seq_len, 10)
    
    for rando in randos:
        seed_text = ' '.join(tokens[rando: rando+seq_len])
        
        args = [model, tokenizer, seq_len, seed_text, num_gen_words]
        generated_text = utils.generate_text(*args)
        
        output_generated_text(seed_text, generated_text, seq_len, f.write)
        
        f.write('\n\n\n')
    
    f.close()

def output_generated_text(seed_text, generated_text, seq_len, output_func):
    if output_func == print:
        kwargs = dict(end="")
    else:
        kwargs = dict()
    
    output_func(seed_text + '\n', **kwargs)
    output_func('='*160 + '\n', **kwargs)
    
    generated_text_tokens = generated_text.split(' ')
    
    i = seq_len
    while i < len(generated_text_tokens):
        output_func(' '.join(generated_text_tokens[i-seq_len:i]), **kwargs)
        output_func('\n', **kwargs)
        i = i + seq_len


if __name__ == '__main__':
    main()