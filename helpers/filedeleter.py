import os

try:
    os.remove('./static/output/joblist')
except:
    pass
try:
    os.remove('./static/output/joblist.csv')
except:
    pass
try:
    os.remove('./static/output/seek.json')
except:
    pass
try:
    os.remove('./static/output/joblist2.csv')
except:
    pass

