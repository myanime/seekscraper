import json
from pandas.io.json import json_normalize
import time

with open('seek.json', 'r') as data:
    seek = json.load(data)

df=json_normalize(seek)
# df = df.drop_duplicates('id')
# df = df.sort('id')
today=time.strftime('_%d_%m_%Y')
filename='./transfer/seek_final{0}.csv'.format(today)
df.to_csv(filename, encoding='utf-8')