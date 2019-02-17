import os
import sys
import pandas as pd
import numpy as np
import datetime as dt

def main(argv):
    file_dt = dt.datetime.now().isoformat()[0:-7].replace(':', '.')
    fname = ('data/loan_cleaned_%s.csv' % file_dt)
    relevant_features = ['issue_d_ord', 'loan_amnt', 'int_rate', 'term',
                         'grade', 'emp_length', 'home_ownership',
                         'annual_inc', 'default']
    df = (pd.read_csv('data/loan.csv', low_memory=False)
          .set_index('id')
          .pipe(status_filter)
          .pipe(remove_annual_inc_nas)
          .pipe(emp_length_filter)
          .query('home_ownership not in ["NONE", "ANY"]')
          .assign(issue_d=lambda x: x.issue_d.astype('datetime64'),
                  default=lambda x: np.where(x.loan_status=='Fully Paid', 0, 1),
                  issue_d_ord=lambda x: x.issue_d.apply(dt.datetime.toordinal),
                  term=lambda x: x.term.str.strip())
          .loc[:, relevant_features]
          .pipe(make_dummy, 'term')
          .pipe(make_dummy, 'home_ownership')
          .pipe(make_dummy, 'emp_length')
          .pipe(make_dummy, 'grade')
          .to_csv(fname))
    print('Luther Preprocessing Successful Woo Woo!\n'
          'See file located at: %s' % fname)

def status_filter(input_df):
    df = input_df.copy()
    statuses = ['Fully Paid', 'Charged Off', 'Default']
    return df.loc[df.loan_status.isin(statuses), ]

def remove_annual_inc_nas(input_df):
    df = input_df.copy()
    return df.loc[~df.annual_inc.isna(), ]

def emp_length_filter(input_df):
    df = input_df.copy()
    na_mask = df.emp_length.isna() | (df.emp_length == 'n/a')
    return df.loc[~na_mask, ]

def make_dummy(input_df, column):
    df = input_df.copy()
    home_dum = (df.loc[:, [column]].pipe(pd.get_dummies))
    return df.join(home_dum).drop(column, axis=1)

if __name__ == '__main__':
    main(sys.argv)
