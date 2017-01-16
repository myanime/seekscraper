import json
from pandas.io.json import json_normalize
import time
import os

with open('seek.json', 'r') as data:
    seek = json.load(data)

# print len(seek)
# unique = {each['name']['id']: each for each in seek}.values()
# print len(unique)
unique = seek

df=json_normalize(unique)
# df = df.drop_duplicates('name.id')
# df = df.sort('name.id')
today=time.strftime('_%d_%m_%Y')
filename='./transfer/seek_final{0}.csv'.format(today)
df.to_csv(filename, encoding='utf-8')

#Deduplicated
# with open('seek.json', 'w') as data:
#     json.dump(unique, data)