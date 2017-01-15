import json
from pandas.io.json import json_normalize
import time
import os

for x in range(1, 15):
    with open('{0}new_jobs.json'.format(x), 'r') as data:
        all_jobs = json.load(data)

    unique = {each['name']['id']: each for each in all_jobs}.values()

    with open('{0}a_new_jobs.json'.format(x), 'w') as data:
        json.dump(unique, data)

    os.remove('./{0}new_jobs.json'.format(x))

with open('seek.json', 'r') as data:
    seek = json.load(data)

all_jobs = None
for x in range(1, 15):
    with open('{0}a_new_jobs.json'.format(x), 'r') as data:
        new_jobs = json.load(data)
        print len(new_jobs), 'file:', x
        if not all_jobs:
            all_jobs = new_jobs
            continue
        all_jobs = all_jobs + new_jobs

# all_jobs = jmerge(seek, new_jobs)

print len(seek)
print len (all_jobs)
unique = {each['name']['id']: each for each in all_jobs}.values()
print len(unique)

df=json_normalize(unique)
df = df.drop_duplicates('name.id')
df = df.sort('name.id')
today=time.strftime('_%d_%m_%Y')
filename='./transfer/seek_serversplit{0}.csv'.format(today)
df.to_csv(filename, encoding='utf-8')

#Deduplicated
with open('seek.json', 'w') as data:
    json.dump(unique, data)

for x in range(1, 15):
    os.remove('./{x}a_new_jobs.json'.format(x))