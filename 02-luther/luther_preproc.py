import os
import re
import pandas
import statsmodels.api as sm
import statsmodels.formula as smf
import patsy

files = [x for x in os.listdir('data') if re.match('box_office_mojo_data', x)]
df = pd.read_csv('data/%s' % sorted(files)[0]).set_index('title')

df.info()

df.dtypes

def fmt_runtime(col):
    return (col.str.split(' ', expand=True)
            .iloc[:, [0, 2]]
            .apply(pd.to_numeric)
            .apply(lambda row: row[0] * 60 + row[2], axis=1))

def ctoi(col):
    return col.str.replace('$', '').str.replace(',', '').astype('int64')

def ctol(col):
    return (col.str.replace('$', '')
            .str.replace(',', '')
            .str.replace(' million', '')
            .astype('float64'))

df = (df.loc[~df.budget.isna(), ]
      .assign(open_wkend_gross=lambda x: ctoi(x.open_wkend_gross),
              budget=lambda x: ctol(x.budget) * 1000000,
              release_date=lambda x: x.release_date.astype('datetime64'),
              runtime=lambda x: fmt_runtime(x.runtime)))

# TODO: make genre dummy
df.genre.unique()

# TODO: make rating dummy
df.rating.unique()

# TODO: make distributor dummy
df.distributor.unique()
df.distributor.value_counts()

# TODO: figure out something for actors

# TODO: figure out something for directors

# TODO: in_release
