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
from xgboost import XGBClassifier
%pylab

pat = re.compile('loan_cleaned_')
fname = sorted([x for x in os.listdir('data') if pat.match(x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .set_index('id'))

X = df.drop('default', axis=1)
y = df['default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
                                                    stratify=y, random_state=0)

clf = XGBClassifier()
clf.fit(X_train, y_train)
mcu.ClassifierDiagnostics(clf, X_test, y_test)
