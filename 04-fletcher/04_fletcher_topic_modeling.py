# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 09:43:38 2020

@author: Brendan Non-Admin
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from langdetect import detect
import nltk
from nltk.corpus import stopwords
import spacy
from kickstarter_utils import create_df_topic_word_lists, show_random_pitch

##############################################################################
# Stop Words
##############################################################################
show_random_pitch()

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

##############################################################################
# First model
##############################################################################
x = df.loc[:, 'story']
cv = CountVectorizer(max_df=0.9, min_df=2, stop_words=full_stopwords)
dtm = cv.fit_transform(x)

lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(dtm)

topic_results = lda.transform(dtm)
df.loc[:, 'topic_id'] = topic_results.argmax(axis=1) + 1

args = [lda, cv, df,]
create_df_topic_word_lists(*args, verbose=True) 

##############################################################################
# Remove other languages
##############################################################################
df.loc[:, 'language'] = df.loc[:, 'story'].apply(lambda x: detect(str(x)))

non_english_lang_mask = df.loc[:, 'language'] != 'en'
columns = ['story', 'language']
df.loc[non_english_lang_mask, columns]

mask = df.loc[:, 'language'] == 'en'
df = df.loc[mask, ]
assert((df.language == 'en').all())

# remove ones that still have some spanish in them
mask = ~df.story.str.contains(' este ')
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

df.loc[:, 'topic_id'] = topic_results.argmax(axis=1) + 1

args = [lda, cv, df,]
df_topic_word_lists = create_df_topic_word_lists(*args, n=15, verbose=False)

mask = df.loc[: , 'topic_id'].isin([7, 8])
columns = ['topic_id', 'project_description']
(df.loc[mask, columns]
    .set_index('topic_id')
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
df.loc[:, 'topic'] = df.loc[:, 'topic_id'].map(topic_labels)

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

def lemma_check(token):
    return token.pos_ in relevant_pos and token.lemma_ != '-PRON-'

def spacy_preprocessing(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if lemma_check(token)]
    return " ".join(lemmas)

x = df.loc[:, 'story'].apply(spacy_preprocessing)

cv = CountVectorizer(max_df=0.9, min_df=30, stop_words=full_stopwords)
dtm = cv.fit_transform(x) # dtm = document-term matrix

for n_component in range(6, 14, 2):
    lda = LatentDirichletAllocation(n_components=n_component, random_state=42)
    lda.fit(dtm)

    topic_results = lda.transform(dtm)
    df.loc[:, 'topic_id'] = topic_results.argmax(axis=1) + 1

    with open(f"Data/lda_model_with_{n_component}_topics.txt", 'w') as f:
        args = [lda, cv, df,]
        df_topic_word_lists = create_df_topic_word_lists(*args, n=20, f=f)

##############################################################################
# Try NMF model uses the 10 topic category
##############################################################################

tfidf_kwargs = dict(
    max_df=0.95, 
    min_df=10, 
    stop_words=full_stopwords,
)
tfidf_vectorizer = TfidfVectorizer(**tfidf_kwargs)
tfidf = tfidf_vectorizer.fit_transform(x)
n_components = 10
nmf = NMF(n_components=n_components, random_state=42).fit(tfidf)

topic_results = nmf.transform(tfidf)
df.loc[:, 'topic_id'] = topic_results.argmax(axis=1) + 1

with open(f"Data/nmf_model_with_10_topics.txt", 'w') as f:
    args = [nmf, tfidf_vectorizer, df,]
    df_topic_word_lists = create_df_topic_word_lists(*args, n=20, f=f)
    

##############################################################################
# Final LDA model uses the 10 topic category
##############################################################################
lda = LatentDirichletAllocation(n_components=n_component, random_state=42)
lda.fit(dtm)

topic_results = lda.transform(dtm)
df.loc[:, 'topic_id'] = topic_results.argmax(axis=1) + 1

topic_labels = {
    1: 'design',
    2: 'publishing', 
    3: 'unknown', 
    4: 'games', 
    5: 'comics', 
    6: 'art & fashion',
    7: 'music', 
    8: 'film & video',
    9: 'food',
    10: 'technology',
}
df.loc[:, 'topic'] = df.loc[:, 'topic_id'].map(topic_labels)

##############################################################################
# Compare model results to Kickstarter Categories
##############################################################################
from urllib.parse import unquote

df.loc[:, 'kickstarter_category'] = (df.loc[:, 'category_url']
    .str.replace('https://www.kickstarter.com/discover/categories/', '')
    .str.split('?', expand=True)[0]
    .str.split('/', expand=True)[0]
    .apply(unquote)
)

(df.kickstarter_category
    .value_counts()
    .sort_index()
    .reset_index()
)

mask = df.loc[:, 'topic_id'] == 3
df.loc[mask, 'kickstarter_category'].value_counts(normalize=True)

(df.groupby(['topic', 'kickstarter_category'])
    .size()
    .groupby(level=0).apply(lambda x: x / float(x.sum()))
    .reset_index(name='percent_total')
    .sort_values(['topic', 'percent_total'], ascending=[True, False])
    .to_csv(r'Data/topics_vs_kickstarter_categories.csv', index=False)
)