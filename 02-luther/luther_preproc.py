import os
import sys
import re
import pandas as pd
import numpy as np
import datetime as dt
import patsy


def main(argv):
    files = [x for x in os.listdir('data') if re.match('box_office_mojo_data', x)]
    fname = sorted(files)[-1]
    df = pd.read_csv('data/%s' % fname)#.set_index('title')
    drop_cols = ['actors', 'director', 'distributor', 'url', 'Intercept']
    fname = ('data/box_office_mojo_pp_%s.csv' %
             dt.datetime.now().isoformat()[0:-7])
    mask = (  ~df.budget.isna()
            & ~df.in_release.isna()
            & ~df.domestic_total_gross.isna())
    (df.loc[mask, ]
     .assign(open_wkend_gross=lambda x: ctoi(x.open_wkend_gross),
             domestic_total_gross=lambda x: ctoi(x.domestic_total_gross),
             budget=lambda x: x.budget.apply(budget),
             release_date=lambda x: x.release_date.astype('datetime64'),
             runtime=lambda x: fmt_runtime(x.runtime),
             in_release_days=lambda x: (x.in_release.str.split(expand=True)
                                        [0].astype('int64')),
             widest_release=lambda x: ctoi(x.widest_release),
             log_gross=lambda x: np.log(x.domestic_total_gross))
     .pipe(rating_dum)
     .drop(drop_cols, axis=1)
     .to_csv(fname, index=False))
    print('Luther Preprocessing Successful Woo Woo!')

def budget(x):
    if re.search(r' million', x):
        return int(float(x.replace(' million', '').replace('$', '')) * 1000000)
    else:
        return int(x.replace('$', '').replace(',', ''))

def fmt_runtime(col):
    return (col.str.split(' ', expand=True)
            .iloc[:, [0, 2]]
            .apply(pd.to_numeric)
            .apply(lambda row: row[0] * 60 + row[2], axis=1))

def ctoi(col):
    return (col.str.replace('$', '')
            .str.replace(',', '')
            .astype('int64'))

def ctol(col):
    return (col.str.replace('$', '')
            .str.replace(',', '')
            .astype('float64'))

def rating_dum(input_df):
    df = input_df.copy()
    return df.join(patsy.dmatrix('rating', data=df, return_type='dataframe'))


# TODO: make genre dummy
#df.genre.unique()

# TODO: make distributor dummy
#df.distributor.unique()
#df.distributor.value_counts()

# TODO: figure out something for actors

# TODO: figure out something for directors

# TODO: add Oscars

if __name__ == '__main__':
    main(sys.argv)
