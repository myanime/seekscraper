import time
import pandas as pd
jobid_csv = 'joblist.csv'
jobid_csv2 = 'joblist2.csv'
jobid_csv3 = 'joblist.csv'

with open(jobid_csv, 'rw') as file:
    for line in file:
        line = line.strip('"')
        with open(jobid_csv2,'a') as out:
            out.write(line)
time.sleep(10)
df_month_output = pd.read_csv(jobid_csv2, names = ['jobNumber','salaryRange'], quotechar='!')

df_month_output_deduped = df_month_output.drop_duplicates('jobNumber')

# df_month_output_deduped = df_month_output_deduped.sort('jobNumber')

df_month_output_deduped.to_csv(jobid_csv3, float_format='%.0f', index=False, header=False)