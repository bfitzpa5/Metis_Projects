import os
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import normalize
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
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

drop_cols = ['domestic_total_gross', 'genre', 'open_wkend_gross', 'rating',
             'log_gross', 'release_date', 'in_release']
dummies = ['rating[T.PG]', 'rating[T.PG-13]', 'rating[T.R]']
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
-scores.mean()

reg = LinearRegression()
scores = cross_val_score(reg, X, y, cv=10, scoring='r2', n_jobs=-1)
print(['{:,.2%}'.format(x) for x in scores])
print('Mean R-Squared: {:,.2%}'.format(scores.mean()))

alphas = [0, 1/3**3, 1/3**2, 1/3]
poly = PolynomialFeatures(degree=2)
X_ = poly.fit_transform(X)
print('%-10s%-10s' % ('Alpha', 'R-Squared'))
for alpha in alphas:
    reg = Ridge(alpha=alpha)
    reg.fit(X_, y)
    print('%-10f%-10f' % (alpha, reg.score(X_, y)))

pd.DataFrame({'coefficients': reg.coef_}, index=X_.columns)

alphas = [0, 1/3**3, 1/3**2, 1/3]
poly = PolynomialFeatures(degree=3)
X_ = poly.fit_transform(X)
print('%-10s%-10s' % ('Alpha', 'Mean R-Squared'))
for alpha in alphas:
    reg = Ridge(alpha=alpha)
    reg.fit(X_, y)
    print('%-10f%-10f' % (alpha, reg.score(X_, y)))


kf = KFold(n=len(X), n_folds=5, shuffle=True)

alphas = [3**x for x in range(-1, 6)]
poly = PolynomialFeatures(degree=2)
X_ = poly.fit_transform(X.drop(dummies, axis=1))
columns = poly.get_feature_names(X.drop(dummies, axis=1).columns)
X_ = pd.DataFrame(X_, columns=columns,index=df.index)

#X_, norm = normalize(X_, return_norm=True, axis=0)
#X_ = pd.DataFrame(X_, columns=columns)
print('%-15s%-15s' % ('Alpha', 'Mean R-Squared'))
for alpha in alphas:
    reg = Lasso(alpha=alpha, normalize=True)
    reg.fit(X_, y)
    print('%-15f%-15f' % (alpha, reg.score(X_, y)))


(pd.DataFrame({'coefficients': reg.coef_}, index=X_.columns)
 .assign(coefficients_abs=lambda x: x.coefficients.abs())
 .sort_values(by='coefficients_abs', ascending=False)
 .drop('coefficients_abs', axis=1))
