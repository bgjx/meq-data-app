from django.apps import apps

import pandas as pd
from typing import Tuple

from project import config

def validate_dataframe(df:pd.DataFrame) -> None:
    """
    Raise ValueError if DataFrame is empty or missing required columns.
    """

    if df.empty:
        raise ValueError('DataFrame cannot be empty')
    
    missing_columns = [col for col in config.REQUIRED_COLUMNS_NAME if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing these required columns {', '.join(missing_columns)}")
    

def preprocess_dataframe(df:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extract hypocenter and picking DataFrame from the full DataFrame 
    """

    hypocenter_df = df[[
        "source_id",
        "source_lat_reloc", "source_lon_reloc", "location_reloc", "source_depth_m_reloc", 
        "source_origin_dt_reloc",  "source_err_rms_s_reloc", 
        "source_lat_init", "source_lon_init", "location_init", "source_depth_m_init",
        "source_origin_dt_init",  "source_err_rms_s_init", "gap_init",
        "magnitude"
        ]].drop_duplicates(subset='source_id')
    
    picking_df = df[[
        "source_id", "network_code", "station_code", 
        "station_lat", "station_lon", "station_elev_m",
        "p_arrival_dt", "s_arrival_dt", "coda_dt"
    ]].copy()

    # pre-calculate Ts-Tp for Wadati Profile Calculation
    picking_df['Ts_Tp'] = (picking_df['s_arrival_dt'] - picking_df['p_arrival_dt']).dt.total_seconds()

    return hypocenter_df, picking_df