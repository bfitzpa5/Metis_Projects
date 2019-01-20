import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
%pylab

data_dict = pd.read_excel('data/LCDataDictionary.xlsx')

df = pd.read_csv('data/loan.csv')

df.shape

df.columns

df.loan_status.unique()

df.issue_d.unique()

print("Date Range: %s to %s" % (df.issue_d.min(), df.issue_d.max()))

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
