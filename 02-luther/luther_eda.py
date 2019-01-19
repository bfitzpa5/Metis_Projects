import os
import pandas as pd
import numpy as np
import datetime as dt
import re
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
%pylab

fname = sorted([x for x in os.listdir('data')
                if re.match('box_office_mojo_pp', x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .set_index('title')
      .assign(release_date=lambda x: x.release_date.astype('datetime64'),
              log_gross=lambda x: np.log(x.domestic_total_gross),
              roi=lambda x: x.domestic_total_gross.div(x.budget),
              log_roi=lambda x: np.log(x.roi)))

(df.nlargest(5, 'domestic_total_gross')
 .loc[:, ['domestic_total_gross']])

(df.nlargest(5, 'roi')
 .loc[:, ['roi']])

df.describe().domestic_total_gross

plt.gcf().clear()
order = ['G', 'PG', 'PG-13', 'R']
sns.scatterplot(x='budget', y='domestic_total_gross',
                hue='rating', data=df, hue_order=order)

plt.gcf().clear()
order = ['G', 'PG', 'PG-13', 'R']
sns.scatterplot(x='budget', y='roi',
                hue='rating', data=df, hue_order=order)

plt.gcf().clear()
order = ['G', 'PG', 'PG-13', 'R']
sns.scatterplot(x='budget', y='roi', hue='rating',
                data=df.drop('Paranormal Activity'), hue_order=order)

plt.gcf().clear()
order = ['G', 'PG', 'PG-13', 'R']
sns.boxplot(x='rating', y='domestic_total_gross', data=df, order=order)

plt.gcf().clear()
order = ['G', 'PG', 'PG-13', 'R']
sns.countplot(x='rating', data=df, order=order)

plt.gcf().clear()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(dt.datetime(2008, 1, 1), dt.datetime(2018, 1, 1))
sns.scatterplot(x='release_date', y='domestic_total_gross', hue='rating',
                data=df, ax=ax)

(df.loc[df.release_date.dt.year == 2009, ]
 .nlargest(1, 'domestic_total_gross')
 .loc[:, ['title', 'domestic_total_gross']])

(df.loc[df.release_date.dt.year == 2012, ]
 .nlargest(1, 'domestic_total_gross')
 .loc[:, ['title', 'domestic_total_gross']])

plt.gcf().clear()
sns.distplot(df.domestic_total_gross)

plt.gcf().clear()
sns.distplot(np.cbrt(df.domestic_total_gross).values)

plt.gcf().clear()
sns.distplot(df.log_gross)

plt.gcf().clear()
sns.boxplot(x='year', y='domestic_total_gross',
            data=df.assign(year=lambda x: x.release_date.dt.year))

plt.gcf().clear()
stats.probplot(np.log(df.domestic_total_gross), dist="norm", plot=pylab)

plt.gcf().clear()
stats.probplot(df.domestic_total_gross, dist="norm", plot=pylab)

plt.gcf().clear()
sns.boxplot(x='month', y='domestic_total_gross',
            data=df.assign(month=lambda x: x.release_date.dt.month))

corrcols = ['budget', 'in_release', 'open_wkend_gross', 'rating',
            'release_date', 'runtime', 'widest_release', 'in_release_days',
            'domestic_total_gross']
sns.pairplot(df.loc[:, corrcols])

corrcols = ['budget', 'in_release', 'open_wkend_gross', 'rating',
            'release_date', 'runtime', 'widest_release', 'in_release_days',
            'log_gross']
sns.pairplot(df.loc[:, corrcols])

corrcols = ['budget', 'in_release', 'open_wkend_gross', 'rating',
            'release_date', 'runtime', 'widest_release', 'in_release_days',
            'roi']
sns.pairplot(df.loc[:, corrcols])

corrcols = ['budget', 'in_release', 'open_wkend_gross', 'rating',
            'release_date', 'runtime', 'widest_release', 'in_release_days',
            'roi']
outliers = df.nlargest(5, 'roi').index.tolist()
sns.pairplot(df.drop(outliers).loc[:, corrcols])

corrcols = ['budget', 'in_release', 'open_wkend_gross', 'rating',
            'release_date', 'runtime', 'widest_release', 'in_release_days',
            'log_roi']
sns.pairplot(df.loc[:, corrcols])

corrcols = ['budget', 'in_release', 'open_wkend_gross', 'rating',
            'release_date', 'runtime', 'widest_release', 'in_release_days',
            'log_roi']
outliers = df.nlargest(5, 'roi').index.tolist()
sns.pairplot(df.drop(outliers).loc[:, corrcols])
