import os
import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import luther_util as lu


fname = sorted([x for x in os.listdir('data')
                if re.match('box_office_mojo_pp', x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .set_index('title')
      .assign(release_date=lambda x: x.release_date.astype('datetime64'),
              release_month=lambda x: x.release_date.dt.month,
              release_year=lambda x: x.release_date.dt.year,
              log_gross=lambda x: np.log(x.domestic_total_gross),
              roi=lambda x: x.domestic_total_gross.div(x.budget),
              log_roi=lambda x: np.log(x.roi))
      .query('roi < 15')) # filter out ROI outliers
      
independents = [
    'budget', 
    'domestic_total_gross', 
    'open_wkend_gross',
    'runtime',
    'widest_release', 
    'in_release_days', 
    ['rating[T.PG]', 'rating[T.PG-13]', 'rating[T.R]'], 
    ['release_month', 'release_year']]

results = list()
scoring = 'neg_mean_squared_error'
for variable in independents:
  if isinstance(variable, list):
    X = df.loc[:, variable]
    y = df.loc[:, 'roi']
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    lr = LinearRegression().fit(X_train, y_train)
    scores = lu.lr_scores(lr, X_train, y_train, X_test, y_test)
    mse = -cross_val_score(lr, X, y, cv=10, scoring=scoring).mean()
    lu.add_result(results, variable, scores[0], scores[1], mse)
  else:
    X = df.loc[:, variable].values.reshape(-1, 1)
    y = df.loc[:, 'roi']
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    for degree in range(1, 4):
      if degree == 1:
        lr = LinearRegression().fit(X_train, y_train)
        scores = lu.lr_scores(lr, X_train, y_train, X_test, y_test)
        mse = -cross_val_score(lr, X, y, cv=10, scoring=scoring).mean()
        lu.add_result(results, variable, scores[0], scores[1], mse)
      else:
        lr = make_pipeline(PolynomialFeatures(degree),
                           LinearRegression())
        lr.fit(X_train, y_train)
        scores = lu.lr_scores(lr, X_train, y_train, X_test, y_test)
        mse = -cross_val_score(lr, X, y, cv=10, scoring=scoring).mean()
        lu.add_result(results, variable, scores[0], scores[1], mse, degree)

cols = ['variable', 'degree', 'test_score', 'training_score', 'mse']
results = (pd.DataFrame(results)
           .reindex(columns=cols)
           .assign(rsme=lambda x: np.sqrt(x.mse)))
