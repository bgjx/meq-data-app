from . import config
import pandas as pd

# Data cleanser for catalog data
def clean_hypo_df(df:pd.DataFrame):
    df = df[config.REQUIRED_HYPO_COLUMNS_NAME]

    # convert columns data type
    df['source_id'] = pd.to_numeric(df['source_id'], errors='coerce').astype('Int64')
    df['source_lat'] = pd.to_numeric(df['source_lat'], errors='coerce')
    df['source_lon'] = pd.to_numeric(df['source_lon'], errors='coerce')
    df['source_depth_m'] = pd.to_numeric(df['source_depth_m'], errors='coerce')
    df['source_origin_dt'] = pd.to_datetime(df['source_origin_dt'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    df['source_err_rms_s'] = pd.to_numeric(df['source_err_rms_s'], errors='coerce')
    df['n_phases'] = pd.to_numeric(df['n_phases'], errors='coerce').astype('Int64')
    df['source_gap_degree'] = pd.to_numeric(df['source_gap_degree'], errors='coerce')
    df['x_horizontal_err_m'] = pd.to_numeric(df['x_horizontal_err_m'], errors='coerce')
    df['y_horizontal_err_m'] = pd.to_numeric(df['y_horizontal_err_m'], errors='coerce')
    df['z_depth_err_m'] = pd.to_numeric(df['z_depth_err_m'], errors='coerce')
    df['magnitude'] = pd.to_numeric(df['magnitude'], errors='coerce')
    df['remarks'] = df['remarks'].astype(str).where(df['remarks'].notnull(), None)

    df = df.dropna(subset=['source_id'])

    return df
    