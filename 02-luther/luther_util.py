# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 23:15:29 2019

@author: Brendan Non-Admin
"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

scoring = 'neg_mean_squared_error'

def log_model(results, model, X, y, features, degree=1):
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=0.2, 
                                                        random_state=42)
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    mse = -cross_val_score(model, X, y, cv=10, scoring=scoring).mean()
    record = dict()
    record['features'] = features
    record['degree'] = degree
    record['training_r2'] = train_score
    record['test_r2'] = test_score
    record['mse'] = mse
    results.append(record)
    return results

def format_cols(colname, direction):
    if direction == 'out':
        return (colname.replace('_', ' ')
                .title()
                .replace('Pg', 'PG')
                .replace('Roi', 'ROI')
                .replace('Wkend', 'Weekend'))
    if direction == 'in':
        return (colname.lower()
                .replace(' ', '_')
                .replace('(', '')
                .replace(')', ''))
    raise ValueError('Direction must be "in" or "out"')

from sklearn.base import TransformerMixin, BaseEstimator

class ColumnSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame 
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(self.key, str):
            return X[self.key].values.reshape(-1, 1)
        return X[self.key].values
    
    def get_params(self, deep=True):
        return {'columns': self.key}
    
    def get_feature_names(self):
        return self.key
