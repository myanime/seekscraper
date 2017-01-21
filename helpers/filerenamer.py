import os

try:
    os.rename('./static/output/joblist.csv', './static/output/joblist')
except:
    pass
