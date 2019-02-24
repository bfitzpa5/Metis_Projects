import os
import re
import mcnulty_util as mcu
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from imblearn.combine import SMOTETomek
%pylab

data_dict = pd.read_excel('data/LCDataDictionary.xlsx')

pat = re.compile('loan_cleaned_')
fname = sorted([x for x in os.listdir('data') if pat.match(x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .set_index('id'))

X = df.drop('default', axis=1)
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
                                                    stratify=y, random_state=0)

percent_non_default = (df.default.value_counts()
                       .div(df.shape[0])
                       .apply('{:.3%}'.format)
                       .loc[0, ])
print("Baseline (Percentage of Non-Default) is %s" % percent_non_default)

smt = SMOTETomek(ratio='auto')
X_smt, y_smt = smt.fit_sample(X_train, y_train)
logreg = LogisticRegression(C=100000, solver='lbfgs')
logreg.fit(X_smt, y_smt)
mcu.LogisticDiagnostics(logreg, X_test, y_test)

X_train.columns

non_dummies = ['issue_d_ord', 'loan_amnt', 'int_rate', 'annual_inc', 'dti',
               'open_acc', 'pub_rec', 'revol_bal', 'revol_util',
               'acc_now_delinq']
dummies = [x for x in X_train.columns.tolist() if x not in non_dummies]
ct = ColumnTransformer(
    [('poly', PolynomialFeatures(2), non_dummies),
     ('dummies', 'passthrough', dummies)])
X_train_trans = ct.fit_transform(X_train)
smt = SMOTETomek(ratio='auto')
X_smt, y_smt = smt.fit_sample(X_train_trans, y_train)
logr_p2 = LogisticRegression(C=1, solver='sag', n_jobs=-1,
                             max_iter=100000)
logr_p2.fit(X_smt, y_smt)
