from django.apps import apps

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


mapbox_access_token = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'

REQUIRED_COLUMNS_NAME = [
    "id", "source_id", 
    "source_lat_reloc", "source_lon_reloc", "location_reloc", "source_depth_m_reloc", "source_origin_dt_reloc",
    "source_lat_init", "source_lon_init", "location_init", "source_depth_m_init", "source_origin_dt_init",
    "network_code", "station_code", "station_lat", "station_lon", "station_elev_m",
    "p_arrival_dt", "s_arrival_dt", "coda_dt",
    "n_phases", "magnitude",
    "reloc_remarks", "init_remarks"
]

# get hypocenter catalog
def get_hypocenter_catalog(app_label, slug, catalog_type):
    'Get hypocenter catalog from model.'
    for model in apps.get_app_config(app_label).get_models():
        if f"{slug}_{catalog_type}_catalog" in str(model._meta.db_table):
            all_objects = model.objects.all()
            model_name = model.__name__
            break
    return all_objects, model_name


# get merged catalog view for complete data analysis
def get_merged_catalog(app_label, slug):
    'Get full catalog by merging hypocenter, picking, and station.'
    # get all the tables
    for model in apps.get_app_config(app_label).get_models():
        if f"{slug}_catalog_merged_view" in str(model._meta.db_table):
            all_objects = model.objects.all()
            model_name = model.__name__ 
            break
    return all_objects, model_name


def get_station(app_label, slug):
    'Get station data from station model'
    for model in apps.get_app_config(app_label).get_models():
        if f"{slug}_station" in model._meta.db_table:
            all_objects = model.objects.all()
            break
    return all_objects


def analysis_engine(df: pd.DataFrame):
    'Do data preprocessing and return the data to feed the plotly plots'

    # Check DataFrame integrity
    if df.empty:
        raise ValueError('DataFrame cannot be empty')
    
    missing_columns = [col for col in REQUIRED_COLUMNS_NAME if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing these required columns {', '.join(missing_columns)}")


    
    # Drop duplication for specific columns to get only hypocenter data
    hypocenter_df = df[[
        "source_id", "source_lat_reloc", "source_lon_reloc", "location_reloc", "source_depth_m_reloc", "source_origin_dt_reloc",
        "source_lat_init", "source_lon_init", "location_init", "source_depth_m_init", "source_origin_dt_init",
        "n_phases", "magnitude"]].drop_duplicates(subset='source_id')
    
    picking_df = df[[
        "source_id", "network_code", "station_code", 
        "station_lat", "station_lon", "station_elev_m",
        "p_arrival_dt", "s_arrival_dt", "coda_dt"
    ]]

    # calculate Ts_Tp for Wadati Profile calculation
    picking_df['Ts_Tp'] = (picking_df['s_arrival_dt'] - picking_df['p_arrival_dt']).dt.total_seconds()

    
    # get list of source_id and station
    source_id = hypocenter_df['source_id'].unique()
    stations = sorted(picking_df['station_code'].unique())
    
    # Statistic in number
    total_events = len(hypocenter_df['source_id'])
    total_phases = len(picking_df['p_arrival_dt']) + len(picking_df['s_arrival_dt'])
    total_stations =  len(stations)

    general_statistics = {
        'total_events': total_events,
        'total_phases': total_phases,
        'total_stations': total_stations
    }


    ## Overall Daily intensities
    # get date series from data
    date_series = pd.to_datetime(hypocenter_df['source_origin_dt_init'])
    grouped_daily_data = (date_series
                          .groupby(
                              [
                                date_series.dt.year,
                                date_series.dt.month,
                                date_series.dt.day
                            ]
                          )
                          .size()
                        )
    x_values = [f"{year}-{month:02d}-{day:02d}" for year, month, day in grouped_daily_data.index]
    y_array = grouped_daily_data.values
    y_bar  = y_array.tolist()
    y_cumulative =  np.ndarray.tolist(np.cumsum(y_array))

    overall_daily_intensities = {
        'x_values':x_values,
        'y_bar': y_bar,
        'y_cum': y_cumulative
    }


    ## Station performance
    station_performance = {}
    for sta in stations:
        # select P and S phase data recorded by this station
        phases = picking_df[picking_df['station_code'] == sta][['p_arrival_dt', 's_arrival_dt']] 
        station_performance[f'{sta}'] = {
            'p_phase': len(phases['p_arrival_dt']),
            's_phase': len(phases['s_arrival_dt'])
        }


    ## Station performance time-series
    # create pivot table
    picking_df['p_arrival_dt_date'] = pd.to_datetime(picking_df['p_arrival_dt']).dt.date
    pivot_station  = pd.pivot_table(
                        picking_df,
                        index='p_arrival_dt_date',
                        columns='station_code',
                        aggfunc='size',
                        fill_value=0
    )

    # index manipulation
    pivot_station.index = [f"{index.year}-{index.month:02d}-{index.day:02d}" for index in pivot_station.index]
    time_series_performance = {
        'dates': pivot_station.index.tolist(),
        'stations': pivot_station.columns.tolist(),
        'counts': pivot_station.to_dict('index')
    }


    ## Wadati profile
    # Calculate time reference
    epoch = datetime(1970, 1, 1)

    origin_time = {
        'source_id':[],
        'origin_time': []
    }

    for id in source_id:
        phase_df = picking_df[picking_df['source_id'] == id]
        phase_df = phase_df.copy()

        # calculate total seconds (epoch as reference)
        phase_df['epoch_delta'] = phase_df['p_arrival_dt'].apply(
            lambda x : (x - epoch).total_seconds()
        )
        
        # calculate t_0 with np.polyfit
        z = np.polyfit(phase_df['epoch_delta'], phase_df['Ts_Tp'], 1)
        t_0 = (-1*z[1])/z[0]

        # convert t_0 to datetime object again
        t_0_dt = epoch + timedelta(seconds=t_0)

        origin_time['source_id'].append(id) 
        origin_time['origin_time'].append(t_0_dt)
    
    # calculate P_travel time
    origin_time_df = pd.DataFrame.from_dict(origin_time)

    # merged with the picking_df
    merged = (
                picking_df
                .merge(origin_time_df, on='source_id', how='inner' )
              )
    
    merged['p_travel'] = (merged['p_arrival_dt'] - merged['origin_time']).dt.total_seconds()

    wadati_data = {
        'p_travel': merged['p_travel'].tolist(),
        'ts_tp': merged['Ts_Tp'].tolist()
    }

    # create result objects
    result  = {
        'general_statistics': general_statistics,
        'overall_daily_intensities': overall_daily_intensities,
        'station_performance': station_performance,
        'wadati_profile': wadati_data,
        'time_series_performance': time_series_performance
    }

    return result

