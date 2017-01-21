import time
import pandas as pd
jobid_csv = './pmap.csv'
jobid_csv2 = './pmap2.csv'

df_month_output = pd.read_csv(jobid_csv, names = ['code','city'], quotechar=';')

df_month_output_deduped = df_month_output.drop_duplicates('city')

# df_month_output_deduped = df_month_output_deduped.sort('jobNumber')

df_month_output_deduped.to_csv(jobid_csv2, float_format='%.0f', index=False, header=False)