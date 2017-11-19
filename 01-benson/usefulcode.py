# Libraries
import pandas as pd
import datetime as dt


turnstiles_df["DATE_TIME"] = pd.to_datetime(turnstiles_df.DATE + " " + turnstiles_df.TIME, format="%m/%d/%Y %H:%M:%S")

turnstiles_df["DAYOFWEEK"] =turnstiles_df["DATE_TIME"].dt.dayofweek

### Code to pull in multiple turnstile data files
import pandas as pd
from collections import defaultdict
import datetime

# Data from 6/24/17 going back N weeks
datecodes = []
startdate = '20170624'
date = datetime.date(int(startdate[0:4]), int(startdate[4:6]), int(startdate[6:]))
for i in range(2):  ## = N --> Sets number of files to save
    d = date - datetime.timedelta(days=7*i)
    day = str(d.day) if len(str(d.day)) == 2 else '0'+str(d.day)
    month = str(d.month) if len(str(d.month)) == 2 else '0'+str(d.month)
    year = str(d.year)[2:4]

    datecodes.append(year+month+day) 

# Source: http://web.mta.info/developers/turnstile.html
def get_data(datecodes):
    url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt"
    dfs = []
    for datecode in datecodes:
        file_url = url.format(datecode)
        dfs.append(pd.read_csv(file_url))
    return pd.concat(dfs)

df = get_data(datecodes)
df.columns = [column.strip() for column in df.columns]
