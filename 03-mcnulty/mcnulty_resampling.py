import os
import re
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from imblearn.under_sampling import ClusterCentroids
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek
%pylab

fname = sorted([x for x in os.listdir('data')
                if re.match('loan_cleaned_', x)])[-1]
df = pd.read_csv('data/%s' % fname)


X = df.drop('default', axis=1)
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=0, stratify=y)
df_train = X_train.join(y_train)

class_0_count, class_1_count = df_train.default.value_counts()
print('Class Percentages')
print('0: %15.2f%s\n1: %15.2f%s' % (class_0_count/df_train.shape[0], '%',
                                 class_1_count/df_train.shape[0], '%'))

df_under = (df_train.loc[df_train.default == 0, ]
            .sample(class_1_count)
            .append(df_train.loc[df_train.default == 1, ]))
print(df_under.default.value_counts())
X_under = df_under.drop('default', axis=1)
y_under = df_under.default
logr_under = LogisticRegression(C=100000)
logr_under.fit(X_under, y_under)
LogisticDiagnostics(logr_under, X_test, y_test)

df_over = (df_train.loc[df_train.default == 1, ]
           .sample(class_0_count, replace=True)
           .append(df_train.loc[df_train.default == 0, ]))
print(df_over.default.value_counts())
X_over = df_over.drop('default', axis=1)
y_over = df_over.default
logr_over = LogisticRegression(C=100000)
logr_over.fit(X_over, y_over)
LogisticDiagnostics(logr_over, X_test, y_test)

cc = ClusterCentroids(ratio={0:10})
X_cc, y_cc = cc.fit_sample(X_train, y_train)
logr_cc = LogisticRegression(C=100000)
logr_cc.fit(X_cc, y_cc)
LogisticDiagnostics(logr_cc, X_test, y_test)

smote = SMOTE(ratio='minority')
X_sm, y_sm = smote.fit_sample(X_train, y_train)
logr_sm = LogisticRegression(C=100000)
logr_sm.fit(X_sm, y_sm)
LogisticDiagnostics(logr_sm, X_test, y_test)

smt = SMOTETomek(ratio='auto')
X_smt, y_smt = smt.fit_sample(X_train, y_train)
logr_smt = LogisticRegression(C=100000)
logr_smt.fit(X_smt, y_smt)
LogisticDiagnostics(logr_smt, X_test, y_test)
