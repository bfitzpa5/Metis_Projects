import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
%pylab

data_dict = pd.read_excel('data/LCDataDictionary.xlsx')

def status_filter(input_df):
    df = input_df.copy()
    statuses = ['Fully Paid', 'Charged Off', 'Default']
    return df.loc[df.loan_status.isin(statuses), ]

def remove_annual_inc_nas(input_df):
    df = input_df.copy()
    return df.loc[~df.annual_inc.isna(), ]

def emp_length_filter(input_df):
    df = input_df.copy()
    na_mask = df.emp_length.isna() | (df.emp_length == 'n/a')
    return df.loc[~na_mask, ]

def make_dummy(input_df, column):
    df = input_df.copy()
    home_dum = (df.loc[:, [column]].pipe(pd.get_dummies))
    return df.join(home_dum).drop(column, axis=1)

relevant_features = ['issue_d_ord', 'loan_amnt', 'int_rate', 'term',
                     'grade', 'emp_length', 'home_ownership',
                     'annual_inc', 'default']
df = (pd.read_csv('data/loan.csv', low_memory=False)
      .assign(issue_d=lambda x: x.issue_d.astype('datetime64'))
      .pipe(status_filter)
      .pipe(remove_annual_inc_nas)
      .pipe(emp_length_filter)
      .query('home_ownership not in ["NONE", "ANY"]')
      .assign(default=lambda x: np.where(x.loan_status=='Fully Paid', 0, 1),
              issue_d_ord=lambda x: x.issue_d.apply(dt.datetime.toordinal),
              term=lambda x: x.term.str.strip())
      .loc[:, relevant_features]
      .pipe(make_dummy, 'term')
      .pipe(make_dummy, 'home_ownership')
      .pipe(make_dummy, 'emp_length')
      .pipe(make_dummy, 'grade'))

df.columns

X = df.drop('default', axis=1)
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

logreg = LogisticRegression(C=100000)
logreg.fit(X_train, y_train)
accuracy_train = logreg.score(X_train, y_train)
accuracy_test = logreg.score(X_test, y_test)
print("train_score=%.3f\ntest_score =%.3f\n" % (accuracy_train*100, accuracy_test*100))

logreg.intercept_

percent_non_default = (df.default.value_counts()
                       .div(df.shape[0])
                       .apply('{:.3%}'.format)
                       .loc[0, ])
print("Baseline (Percentage of Non-Default) is %s" % percent_non_default)

df.loc[:, 'mths_since_last_delinq'].value_counts()

