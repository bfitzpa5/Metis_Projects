import os
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from matplotlib import pyplot as plt
import time

def main():
    filename = os.path.join('data', 'lending_club_clean.csv')
    df = pd.read_csv(filename, index='id')
    df, le_emp_length = label_encoding_helper(df, 'emp_length')
    df, le_term = label_encoding_helper(df, 'term')
    df, le_purpose = label_encoding_helper(df, 'purpose')
    df, le_grade = label_encoding_helper(df, 'grade')

    features = [
        'loan_amnt', 'int_rate', 'annual_inc', 'dti',
        'emp_length', 'term', 'purpose', 'grade'
    ]
    dependent = 'default'
    model_name = 'Random Forest'
    X, y = df.loc[:, features], df.loc[:, dependent]

    tts_params = dict(test_size=0.33, random_state=42, stratify=y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, **tts_params)

    param_grid = {
        'bootstrap': [True],
        'max_depth': [10, 100, 1000],
        'max_features': [2, 4, 'auto'],
        'min_samples_leaf': [2**x for x in range(1, 4)],
        'min_samples_split': [2**x for x in range(3, 5)],
        'n_estimators': [2**x for x in range(8, 12)]
    }
    rf = RandomForestClassifier(n_jobs=-1)
    gs = GridSearchCV(rf, param_grid, scoring='f1', cv=5, verbose=15, n_jobs=-1)

    start_time = time.time()
    gs.fit(X_train, y_train)
    end_time = time.time()

    elapsed_time = end - start
    print("Wall Time: {:,.0f}".format(elapsed_time))


def label_encoding_helper(input_df, column):
    df = input_df.copy()
    x = df.loc[:, column]

    le = LabelEncoder()
    le.fit(x)
    df.loc[:, column] = le.transform(x)

    return df, le

if __name__ == '__main__':
    main()
