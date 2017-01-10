import json
from pandas.io.json import json_normalize
import time
import os

with open('1new_jobs.json', 'r') as data:
    all_jobs = json.load(data)

unique = {each['name']['id']: each for each in all_jobs}.values()

with open('1a_new_jobs.json', 'w') as data:
    json.dump(unique, data)

os.remove('./1new_jobs.json')

with open('2new_jobs.json', 'r') as data:
    all_jobs = json.load(data)

unique = {each['name']['id']: each for each in all_jobs}.values()

with open('2a_new_jobs.json', 'w') as data:
    json.dump(unique, data)

os.remove('./2new_jobs.json')

with open('3new_jobs.json', 'r') as data:
    all_jobs = json.load(data)

unique = {each['name']['id']: each for each in all_jobs}.values()

with open('3a_new_jobs.json', 'w') as data:
    json.dump(unique, data)

os.remove('./3new_jobs.json')

with open('seek.json', 'r') as data:
    seek = json.load(data)

with open('1a_new_jobs.json', 'r') as data:
    new_jobs1 = json.load(data)

with open('2a_new_jobs.json', 'r') as data:
    new_jobs2 = json.load(data)

with open('3a_new_jobs.json', 'r') as data:
    new_jobs3 = json.load(data)

all_jobs = seek + new_jobs1 + new_jobs2 + new_jobs3
# all_jobs = jmerge(seek, new_jobs)

print len(seek)
print len(new_jobs1)
print len(new_jobs2)
print len(new_jobs3)
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

os.remove('./1a_new_jobs.json')
os.remove('./2a_new_jobs.json')
os.remove('./3a_new_jobs.json')