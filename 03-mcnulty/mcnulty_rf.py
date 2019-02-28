%load_ext autoreload
%autoreload 2
import os
import re
import mcnulty_util as mcu
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.combine import SMOTETomek
%pylab

def plot_feature_importances(clf, colnames):
    data = {'features': colnames,
            'importance': clf.feature_importances_}
    impt = (pd.DataFrame(data)
            .sort_values('importance', ascending=False))
    sns.barplot(x='importance', y='features', order=impt.features, data=data)

pat = re.compile('loan_cleaned_')
fname = sorted([x for x in os.listdir('data') if pat.match(x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .set_index('id'))

X = df.drop('default', axis=1)
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
                                                    stratify=y, random_state=0)


clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
mcu.ClassifierDiagnostics(clf, X_test, y_test)
plot_feature_importances(clf, X_train.columns)

smt = SMOTETomek(ratio='auto')
X_smt, y_smt = smt.fit_sample(X_train, y_train)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_smt, y_smt)
mcu.ClassifierDiagnostics(clf, X_test, y_test)
plot_feature_importances(clf, X_smt.columns)
