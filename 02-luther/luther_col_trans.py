# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 12:45:06 2019

@author: Brendan Non-Admin
"""

import os
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn import metrics
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
      

ivars = [
  'budget', 
  'domestic_total_gross', 
  'open_wkend_gross',
  'runtime',
  'widest_release', 
  'in_release_days', 
  'rating', 
  'release_month',
  'release_year']
dvar = ['log_roi']

X = df.loc[:, ivars]
y = df.loc[:, dvar]
X_train, X_test, y_train, y_test = train_test_split(X, y)

rating = Pipeline([
  ('selector', lu.ColumnSelector(key='rating')),
  ('ohe', OneHotEncoder()),
  ])

passthroughs = ['release_month', 'release_year', 'runtime']
passthroughs = lu.ColumnSelector(key=passthroughs)

budget = Pipeline([
  ('selector', lu.ColumnSelector(key='budget')),
  ('poly', PolynomialFeatures(degree=2, include_bias=False)),
  ])

feats = FeatureUnion([
  ('rating', rating),
  ('budget', budget),
  ('passthroughs', passthroughs)
  ])

est = Pipeline([
  ('features', feats),
  ('lr', LinearRegression())
  ])

est.fit(X_train, y_train)

est.score(X_test, y_test)

est['lr'].coef_

est['lr'].intercept_