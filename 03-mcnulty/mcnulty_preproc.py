import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
%pylab

data_dict = pd.read_excel('data/LCDataDictionary.xlsx')

"""
df = (pd.read_csv('data/loan.csv')
      .assign(issue_d_datetime=lambda x: x.issue_d.astype('datetime64')))

(df.loc[:, ['issue_d', 'issue_d_datetime']]
 .drop_duplicates()
 .sort_values('issue_d_datetime')
 .to_csv(os.path.join('data', 'datetime_test.csv')))
"""

df = (pd.read_csv('data/loan.csv')
      .assign(issue_d=lambda x: x.issue_d.astype('datetime64')))

print("Date Range: %s to %s" % (df.issue_d.min().isoformat()[:-9],
                                df.issue_d.max().isoformat()[:-9]))

df.loan_status.unique()

df.loan_status.value_counts().plot.bar()

(df.loc[df.loan_status.str.contains('Does not'), ['issue_d']]
 .drop_duplicates()
 .sort_values(by='issue_d'))

""" note to BF, figure out way to color bars """
xticks = df.issue_d.drop_duplicates().sort_values().dt.strftime('%Y-%m').values
ax = df.issue_d.value_counts().plot.bar()
ax.set_xticklabels(xticks)

df.loan_status.value_counts()

plt.gcf().clear()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticklabels(labels=df.loan_status, rotation=90)
sns.countplot('loan_status', data=df)

loan_statuses = ['Default', 'Fully Paid']
df  = df.loc[df.loan_status.isin(loan_statuses), ]

plt.gcf().clear()
sns.countplot('grade', data=df)

plt.gcf().clear()
sns.scatterplot(x='annual_inc', y='loan_amnt',
                hue='loan_status', data=df)

plt.gcf().clear()
sizes = {'Fully Paid': 20, 'Default': 100}
sns.scatterplot(x='annual_inc', y='loan_amnt', hue='loan_status',
                style='loan_status', size='loan_status', sizes=sizes,
                data=df.loc[df.annual_inc < 400000, ])

plt.gcf().clear()
sns.boxplot(x='loan_status', y='annual_inc', data=df.loc[df.annual_inc < 400000, ])

plt.gcf().clear()
sns.boxplot(x='loan_status', y='loan_amnt', data=df.loc[df.annual_inc < 400000, ])

df = df.loc[df.annual_inc < 400000, ]

plt.gcf().clear()
sns.countplot(x='loan_status', hue='term', data=df)
