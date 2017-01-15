import json
import os
filename = "13"

with open(filename + 'new_jobs.json', 'r') as data:
    all_jobs = json.load(data)
unique = {each['name']['id']: each for each in all_jobs}.values()

with open(filename +'a_new_jobs.json', 'w') as data:
    json.dump(unique, data)

os.remove('./filename + new_jobs.json')
