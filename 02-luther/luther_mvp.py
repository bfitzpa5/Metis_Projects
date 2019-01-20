import os
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
%pylab

fname = sorted([x for x in os.listdir('data')
                if re.match('box_office_mojo_pp', x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .assign(release_date=lambda x: x.release_date.astype('datetime64'),
              log_gross=lambda x: np.log(x.domestic_total_gross)))

(df.drop('domestic_total_gross', axis=1)
 .corr()['log_gross'].abs().sort_values(ascending=False))

lm1 = smf.ols('log_gross ~ open_wkend_gross', data=df)
fit1 = lm1.fit()
fit1.summary()

lm2 = smf.ols('domestic_total_gross ~ widest_release', data=df)
fit2 = lm2.fit()
fit2.summary()

lm3 = smf.ols('log_gross ~ widest_release + runtime', data=df)
fit3 = lm3.fit()
fit3.summary()

plt.gcf().clear()
fit3.resid.plot(style='o')

lm4 = smf.ols('log_gross ~ widest_release + runtime + widest_release*runtime', data=df)
fit4 = lm4.fit()
fit4.summary()

lm3 = smf.ols('log_gross ~ widest_release + runtime', data=df)
fit3 = lm3.fit()
fit3.summary()

