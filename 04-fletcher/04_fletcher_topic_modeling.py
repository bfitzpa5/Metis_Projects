# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 09:43:38 2020

@author: Brendan Non-Admin
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from langdetect import detect

##############################################################################
# Cleaning
##############################################################################
path = 'Data/kickstarter_data.json'
df = pd.read_json(path)

df.head()

mask = ~df.loc[:, 'story'].isnull() & (df.loc[:, 'story'] != '')
df = df.loc[mask, :]

def topic_word_lists(lda, n=10, verbose=False):
    topic_word_lists = list()
    components = lda.components_
    for i, topic in enumerate(components):
        word_list = [cv.get_feature_names()[index] for index in topic.argsort()[-n:]]
        topic_word_lists.append(word_list)
        if verbose:
            print(f"The TOP {n} WORDS FOR TOPIC #{i}")
            print(word_list)
            print('\n\n')
    columns = ['Word {}'.format(x) for x in range(1, n+1)]
    index = ['Topic {}'.format(x) for x in range(1, len(components)+1)]
    return pd.DataFrame(topic_word_lists, index, columns)

##############################################################################
# First model
##############################################################################
x = df.loc[:, 'story']
cv = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')
dtm = cv.fit_transform(x)

lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(dtm)

topic_word_lists(lda, verbose=True) 

topic_results = lda.transform(dtm)
df.loc[:, 'Topic'] = topic_results.argmax(axis=1)

##############################################################################
# Remove other languages
##############################################################################
df.loc[:, 'language'] = df.loc[:, 'story'].apply(lambda x: detect(str(x)))

non_english_lang_mask = df.loc[:, 'language'] != 'en'
columns = ['story', 'language']
df.loc[non_english_lang_mask, columns]

mask = df.loc[:, 'language'] == 'en'
df = df.loc[mask, ]

##############################################################################
# Second model
##############################################################################
x = df.loc[:, 'story']
cv = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')
dtm = cv.fit_transform(x)

lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(dtm)

twl = topic_word_lists(lda, verbose=False)
twl

topic_results = lda.transform(dtm)
df.loc[:, 'Topic'] = topic_results.argmax(axis=1)

##############################################################################
# Third model - with SpaCy
##############################################################################

# TODO


