import pandas
import os
import re

files = [x for x in os.listdir('data') if re.match('box_office_mojo_data', x)]
df = pd.read_csv('data/%s' % sorted(files)[0]).set_index('title')
