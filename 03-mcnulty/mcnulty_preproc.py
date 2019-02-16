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

df = (pd.read_csv('data/loan.csv', low_memory=False)
      .assign(issue_d=lambda x: x.issue_d.astype('datetime64'))
      .pipe(status_filter)
      .assign(default=lambda x: np.where(x.loan_status=='Fully Paid', 0, 1)))


df.loc[df.funded_amnt.isna(), ]

features = ['funded_amnt']
X = df[features]
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)



logreg = LogisticRegression(C=100000)
logreg.fit(X_train, y_train)
accuracy_train = logreg.score(X_train, y_train)
accuracy_test = logreg.score(X_test, y_test)
print("train_score=%.3f\ntest_score =%.3f\n" % (accuracy_train*100, accuracy_test*100))

(df.default.value_counts() / df.shape[0]).apply('{:.3%}'.format)
