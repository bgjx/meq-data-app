import pandas as pd
from datetime import datetime
from pathlib import Path

# read the csv file
csv_path = Path(r"C:\Users\arham zakki edelo\meq-webapp\databases\hypo_wcc.csv")

# load to dataframe
df_csv = pd.read_csv(csv_path, delimiter = ';')

df_dt_converted = []
for _id in list(df_csv.get("id")):
    col = df_csv[df_csv.id == _id].iloc[0]
    dt_raw = f"{int(col.year)}-{int(col.month):02d}-{int(col.day):02d} {int(col.hour):02d}:{int(col.minute):02d}:{float(col.second):08.5f}"
    cv_to_dt = datetime.strptime(dt_raw, "%Y-%m-%d %H:%M:%S.%f" )
    df_dt_converted.append(cv_to_dt)

df_csv['dt_origin'] = df_dt_converted
df_csv = df_csv[['id', 'lat', 'lon', 'utm_x_m', 'utm_y_m', 'depth_m', 'elev_m', 'year', 'month', 'day', 'hour', 'minute', 'second', 'dt_origin', 'rms_error', 'ml_mag', 'mw_mag', 'remarks']]
df_csv.to_csv("hypo_wcc_dt_converted.csv", sep = ',', index=False)
