# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 09:43:38 2020

@author: Brendan Non-Admin
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from langdetect import detect
import nltk
from nltk.corpus import stopwords
import spacy

nltk.download('stopwords')

##############################################################################
# Stop Words
##############################################################################
custom_stopwords = ['kickstarter', 'pledge', 'project', 'backer', 'campaign']
full_stopwords = stopwords.words('english') + custom_stopwords

##############################################################################
# Cleaning
##############################################################################
path = 'Data/kickstarter_data.json'
df = pd.read_json(path)

df.head()

mask = ~df.loc[:, 'story'].isnull() & (df.loc[:, 'story'] != '')
df = df.loc[mask, :]

def create_df_topic_word_lists(lda, n=10, verbose=False):
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
cv = CountVectorizer(max_df=0.9, min_df=2, stop_words=full_stopwords)
dtm = cv.fit_transform(x)

lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(dtm)

create_df_topic_word_lists(lda, verbose=True) 

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
cv = CountVectorizer(max_df=0.9, min_df=2, stop_words=full_stopwords)
dtm = cv.fit_transform(x)

lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(dtm)

topic_results = lda.transform(dtm)

df_topic_word_lists = create_df_topic_word_lists(lda, n=15, verbose=False)

df.loc[:, 'Topic ID'] = topic_results.argmax(axis=1) + 1

df.loc[:, 'Topic ID'].value_counts()

mask = df.loc[: , 'Topic ID'].isin([7, 8])
columns = ['Topic ID', 'project_description']
(df.loc[mask, columns]
    .set_index('Topic ID')
    .sort_index()
)

topic_labels = {
    1: 'film & video',
    2: 'design', 
    3: 'comics', 
    4: 'children\'s books', 
    5: 'board games', 
    6: 'card games',
    7: 'crafts', 
    8: 'unknown',
    9: 'other languages',
    10: 'technology',
}
df.loc[:, 'Topic'] = df.loc[:, 'Topic ID'].map(topic_labels)

##############################################################################
# Third model - with SpaCy
##############################################################################

nlp = spacy.load("en_core_web_sm")
relevant_pos = [
    'ADJ',
    'ADV',
    'NOUN',
    'VERB',  
]

def spacy_preprocessing(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if token.pos_ in relevant_pos and token.lemma_ != '-PRON-']
    return " ".join(lemmas)

x = df.loc[:, 'story'].apply(spacy_preprocessing)

cv = CountVectorizer(max_df=0.9, min_df=2, stop_words=full_stopwords)
dtm = cv.fit_transform(x)

lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(dtm)

topic_results = lda.transform(dtm)
df.loc[:, 'Topic ID'] = topic_results.argmax(axis=1) + 1
df.loc[:, 'Topic ID'].value_counts()

df_topic_word_lists = create_df_topic_word_lists(lda, n=15, verbose=False)
df_topic_word_lists

topic_labels = {
    1: 'film',
    2: 'design', 
    3: 'publishing', 
    4: 'games', 
    5: 'technology', 
    6: 'design',
    7: 'unknown', 
    8: 'unknown',
    9: 'music',
    10: 'food',
}
df.loc[:, 'Topic'] = df.loc[:, 'Topic ID'].map(topic_labels)

mask = df.loc[:, 'Topic ID'] == 10
(df.loc[mask, 'category_url']
    .str.replace('https://www.kickstarter.com/discover/categories/', '')
    .str.split('?', expand=True)[0]
)