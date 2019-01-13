import os
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
%pylab

fname = sorted([x for x in os.listdir('data')
                if re.match('box_office_mojo_pp', x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .assign(release_date=lambda x: x.release_date.astype('datetime64'),
              log_gross=lambda x: np.log(df.domestic_total_gross)))

df.nlargest(5, 'domestic_total_gross').loc[:, 'title']

df.describe().domestic_total_gross

plt.gcf().clear()
sns.scatterplot(x='budget', y='domestic_total_gross', hue='rating', data=df)

plt.gcf().clear()
sns.boxplot(x='rating', y='domestic_total_gross', data=df)

plt.gcf().clear()
sns.scatterplot(x='release_date', y='domestic_total_gross', data=df)

plt.gcf().clear()
sns.scatterplot(x='release_date', y='domestic_total_gross', hue='rating', data=df)

plt.gcf().clear()
sns.distplot(df.domestic_total_gross)

plt.gcf().clear()
sns.distplot(np.log(df.domestic_total_gross))

plt.gcf().clear()
sns.distplot(np.cbrt(df.domestic_total_gross).values)

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
            'log_gross']
sns.pairplot(df.loc[:, corrcols])

corrcols = ['budget', 'in_release', 'open_wkend_gross', 'rating',
            'release_date', 'runtime', 'widest_release', 'in_release_days',
            'domestic_total_gross']
sns.pairplot(df.loc[:, corrcols])
