import json
from pandas.io.json import json_normalize
import time
import pandas as pd
post_codes_csv = 'post_codes.csv'
with open('seek.json', 'r') as data:
    seek = json.load(data)

df=json_normalize(seek)

df_post_codes = pd.read_csv(post_codes_csv, delimiter=';')
df_month_output_deduped = df.merge(df_post_codes, on='locationWhereValue', how='left')

# df = df.drop_duplicates('id')
# df = df.sort('id')
today=time.strftime('_%d_%m_%Y')
filename='./transfer/seek_final{0}.csv'.format(today)
df_month_output_deduped.to_csv(filename, encoding='utf-8')