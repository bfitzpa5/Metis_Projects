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
df = pd.read_csv('data/%s' % fname)


df.corr()['domestic_total_gross'].abs().sort_values(ascending=False)

np.log(df.budget).plot.box()

lm1 = smf.ols('domestic_total_gross ~ open_wkend_gross', data=df)
fit1 = lm1.fit()
fit1.summary()

lm2 = smf.ols('domestic_total_gross ~ widest_release + runtime', data=df)
fit2 = lm2.fit()
fit2.summary()

lm3 = smf.ols('log_gross ~ widest_release + runtime', data=df)
fit3 = lm3.fit()
fit3.summary()

lm4 = smf.ols('log_gross ~ widest_release + runtime + widest_release*runtime', data=df)
fit4 = lm4.fit()
fit4.summary()
