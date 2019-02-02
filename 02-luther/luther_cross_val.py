import os
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import scipy.stats as stats
%pylab

fname = sorted([x for x in os.listdir('data')
                if re.match('box_office_mojo_pp', x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .assign(release_date=lambda x: x.release_date.astype('datetime64'),
              log_gross=lambda x: np.log(x.domestic_total_gross),
              widest_release_sq=lambda x: x.widest_release**2,
              release_date_julian=lambda x: (x.release_date.dt.strftime('%y%j')
                                             .astype('int64')))
      .set_index('title'))

df.columns
drop_cols = ['domestic_total_gross', 'genre', 'open_wkend_gross', 'rating',
             'log_gross', 'release_date', 'in_release']
X = df.drop(drop_cols, axis=1)
y = df.loc[:, 'log_gross']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
lr = LinearRegression()
lr.fit(X_train, y_train)
lr.score(X_train, y_train)
lr.score(X_test, y_test)

k_fold = KFold(n_splits=10)
reg = LinearRegression()
scores = cross_val_score(reg, X, y, cv=k_fold, scoring='neg_mean_squared_error',
                         n_jobs=-1)
print(-scores)
np.sqrt(-scores).mean() / y.mean()

reg.predict(X.iloc[3])

reg = LinearRegression()
scores = cross_val_score(reg, X, y, cv=10, scoring='r2', n_jobs=-1)
print(['{:,.2%}'.format(x) for x in scores])
print('Mean R-Squared: {:,.2%}'.format(scores.mean()))

y = df.loc[:, 'domestic_total_gross']
k_fold = KFold(n_splits=10)
reg = LinearRegression()
scores = cross_val_score(reg, X, y, cv=k_fold, scoring='neg_mean_squared_error',
                         n_jobs=-1)
print(['{:,.0}'.format(np.sqrt(x)) for x in -scores])
print('{:,.0}'.format(np.sqrt(-scores).mean()))

y = df.loc[:, 'domestic_total_gross']
k_fold = KFold(n_splits=10)
reg = LinearRegression()
scores = cross_val_score(reg, X, y, cv=k_fold, scoring='r2',
                         n_jobs=-1)
print(['{:,.2%}'.format(x) for x in scores])
print('Mean R-Squared: {:,.2%}'.format(scores.mean()))
