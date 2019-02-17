import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
%pylab

data_dict = pd.read_excel('data/LCDataDictionary.xlsx')

fname = sorted([x for x in os.listdir('data')
                if re.match('loan_cleaned_', x)])[-1]
df = pd.read_csv('data/%s' % fname)
X = df.drop('default', axis=1)
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

percent_non_default = (df.default.value_counts()
                       .div(df.shape[0])
                       .apply('{:.3%}'.format)
                       .loc[0, ])
print("Baseline (Percentage of Non-Default) is %s" % percent_non_default)
logreg = LogisticRegression(C=100000)
logreg.fit(X_train, y_train)
accuracy_train = logreg.score(X_train, y_train)
accuracy_test = logreg.score(X_test, y_test)
print("train_score=%.3f\ntest_score =%.3f\n" % (accuracy_train*100, accuracy_test*100))

y_pred = logreg.predict(X_test)
confusion_matrix(y_test, y_pred)
