import time
import pandas as pd
jobid_csv = './static/output/joblist.csv'

df_month_output = pd.read_csv(jobid_csv, names = ['jobNumber','salaryRange'], quotechar='!')

df_month_output_deduped = df_month_output.drop_duplicates('jobNumber')

# df_month_output_deduped = df_month_output_deduped.sort('jobNumber')

df_month_output_deduped.to_csv(jobid_csv, float_format='%.0f', index=False, header=False)