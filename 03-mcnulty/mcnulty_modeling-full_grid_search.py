import os
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from matplotlib import pyplot as plt
import time
import json

def main():
    filename = os.path.join('Data', 'lendingclub_clean.csv')
    df = pd.read_csv(filename, index_col='id')

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

    param_grid = {
        'n_estimators': [2**x for x in range(6, 10)],
        'max_depth': [None] + [2**x for x in range(2, 3)],
        'max_features': ['auto', 'log2'],
        'min_samples_leaf': [2**x for x in range(1, 4)],
        'min_samples_split': [2**x for x in range(1, 4)],
    }
    rf = RandomForestClassifier(n_jobs=-1)
    gs = GridSearchCV(rf, param_grid, scoring='f1', cv=5 verbose=15, n_jobs=-1)

    start_time = time.time()
    gs.fit(X, y)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print("\n\nWall Time: {:,.0f}".format(elapsed_time), end="\n\n")

    write_json(gs.best_params_, "best_params.json")
    print(gs.best_params_, end="\n\n")

    pd.DataFrame(gs.cv_results_).to_csv('cv_results.csv', index=False)
    print(gs.cv_results_, end="\n\n")

def write_json(d, filename):
    json_str = json.dumps(d)
    f = open(filename, "w")
    f.write(json_str)
    f.close()

def label_encoding_helper(input_df, column):
    df = input_df.copy()
    x = df.loc[:, column]

    le = LabelEncoder()
    le.fit(x)
    df.loc[:, column] = le.transform(x)

    return df, le

if __name__ == '__main__':
    main()
