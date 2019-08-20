import os
import sys
import pandas as pd
import numpy as np
import datetime as dt

def main(argv):
    file_dt = dt.datetime.now().isoformat()[0:-7].replace(':', '.')
    fname = ('data/loan_cleaned_%s.csv' % file_dt)
    df = (pd.read_csv('data/loan.csv', low_memory=False)
          .set_index('id')
          .pipe(loan_status_filter)
          .query('application_type == "INDIVIDUAL"')
          .loc[:, features()]
          .assign(issue_d=lambda x: x.issue_d.astype('datetime64'),
                  default=lambda x: np.where(x.loan_status=='Fully Paid', 0, 1),
                  term=lambda x: x.term.str.strip(),
                  emp_length=lambda x: x.emp_length.fillna('Not provided'))
          .pipe(make_dummy, 'term')
          .pipe(make_dummy, 'home_ownership')
          .pipe(make_dummy, 'emp_length')
          .pipe(make_dummy, 'grade')
          .pipe(make_dummy, 'purpose'))
    df.to_csv(fname)
    print('Luther Preprocessing Successful Woo Woo!\n'
          'See file located at: %s' % fname)

def features():
    lc_dd = pd.read_excel(r'data/LCDataDictionary.xlsx')
    qstr = 'Include == 1'
    cols = [x.strip() for x in lc_dd.query(qstr).LoanStatNew.values.tolist()]
    cols.remove('id')
    return cols


def loan_status_filter(input_df):
    df = input_df.copy()
    loan_status_lst = ['Fully Paid', 'Charged Off', 'Late (31-120 days)', 'Default']
    mask = df.loan_status.isin(loan_status_lst)
    return df.loc[mask, :]

def make_dummy(input_df, column):
    df = input_df.copy()
    dummies = (df.loc[:, [column]]
               .pipe(pd.get_dummies))
    return df.join(dummies).drop(column, axis=1)

if __name__ == '__main__':
    main(sys.argv)
