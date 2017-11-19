weekdays = turnstiles_df[(turnstiles_df['DAYOFWEEK'] != 5) & (turnstiles_df['DAYOFWEEK'] != 6)]

df = weekdays.groupby(['C/A', 'UNIT', 'SCP', 'STATION', 'DATE_TIME'], as_index = False).ENTRIES.max()

dfshift = df.shift(1)

df['PREVDT'] = dfshift['DATE_TIME']
df['PREVENT'] = dfshift['ENTRIES']

df = df.iloc[1:]

df['ENTRIESDIFF'] = df['ENTRIES'] - df['PREVENT']
df['TIMEDIFF'] = df['DATE_TIME'] - df['PREVDT']
