import os

try:
    os.remove('./static/output/joblist')
    os.remove('./static/output/seek.json')
except:
    pass