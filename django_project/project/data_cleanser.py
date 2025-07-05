from . import config
import pandas as pd

# Data cleanser for hypo catalog data
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


# Data cleanser for picking catalog data
def clean_picking_df(df:pd.DataFrame):
    df = df[config.REQUIRED_PICKING_COLUMNS_NAME]

    # convert columns data type
    df['source_id'] = pd.to_numeric(df['source_id'], errors='coerce').astype('Int64')
    df['station_code'] = df['station_code'].astype(str).where(df['station_code'].notnull(), None)
    df['p_arrival_dt'] = pd.to_datetime(df['p_arrival_dt'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    df['p_polarity'] = df['p_polarity'].astype(str).where(df['p_polarity'].notnull(), None)
    df['p_onset'] = df['p_onset'].astype(str).where(df['p_onset'].notnull(), None)
    df['s_arrival_dt'] = pd.to_datetime(df['s_arrival_dt'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    df['coda_dt'] = pd.to_datetime(df['coda_dt'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

    df = df.dropna(subset=['source_id'])

    return df

# Data cleanser for picking catalog data
def clean_station_df(df:pd.DataFrame):
    df = df[config.REQUIRED_STATION_COLUMNS_NAME]

    # convert columns data type
    df['station_code'] = df['station_code'].astype(str).where(df['station_code'].notnull(), None)
    df['network_code'] = df['network_code'].astype(str).where(df['network_code'].notnull(), None)
    df['station_lat'] = pd.to_numeric(df['station_lat'], errors='coerce')
    df['station_lon'] = pd.to_numeric(df['station_lon'], errors='coerce')
    df['station_elev_m'] = pd.to_numeric(df['station_elev_m'], errors='coerce')
    
    return df
    
    