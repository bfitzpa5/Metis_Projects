# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:22:13 2020

@author: Brendan Non-Admin
"""


import os
import pandas as pd
import numpy as np
import re

fname = sorted([x for x in os.listdir('data')
                if re.match('box_office_mojo_pp', x)])[-1]
df = (pd.read_csv('data/%s' % fname)
      .set_index('title')
      .assign(release_date=lambda x: x.release_date.astype('datetime64'),
              log_gross=lambda x: np.log(x.domestic_total_gross),
              roi=lambda x: x.domestic_total_gross.div(x.budget) - 1,
              release_year=lambda x: x.release_date.dt.year)
      )

genres = ['Action / Adventure', 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy',
          'Comedy / Drama', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film Noir',
          'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance',
          'Sci-Fi', 'Sport', 'Superhero', 'Thriller', 'War', 'Western']
mask = df.genre.isin(genres)
df = df.loc[mask, ]


dims = ['release_year', 'genre']
measures = ['roi']
df_genre_yearly = (df.groupby(dims).roi.nlargest(1)
    .reset_index()
    .pivot('genre', 'release_year', ['title', 'roi'])
)

dims = ['release_year', 'genre']
measures = ['roi']
df_yearly = (df
    .assign(release_year='total')
    .groupby(dims).roi.nlargest(1)
    .reset_index()
    .pivot('genre', 'release_year', ['title', 'roi'])
)

df_out = df_genre_yearly.join(df_yearly)
columns = [x[0] + '_' + str(x[1]) for x in list(df_out.columns)]
columns = [x.replace('roi', 'max_roi').replace('title', 'title_with_max_roi') for x in columns]
df_out.columns = columns

fout = os.path.join(
  'Data',
  'films_with_largest_roi_by_year.csv'
)
df_out.to_csv(fout)