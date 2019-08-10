# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 23:15:29 2019

@author: Brendan Non-Admin
"""

def lr_scores(model, X_train, y_train, X_test, y_test):
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    return [train_score, test_score]

def add_result(results, variable, training_score, test_score, mse, degree=1):
    record = dict()
    record['variable'] = variable
    record['degree'] = degree
    record['training_score'] = training_score
    record['test_score'] = test_score
    record['mse'] = mse
    results.append(record)
    return results