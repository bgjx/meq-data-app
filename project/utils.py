from django.apps import apps

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress


mapbox_access_token = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'

REQUIRED_COLUMNS_NAME = [
    "id", "source_id", "source_lat_init", "source_lon_init", "location_init",
    "source_depth_m_init", "source_origin_dt_init", "source_err_rms_s_init",
    "remarks_init", "source_lat_reloc", "source_lon_reloc", "location_reloc",
    "source_depth_m_reloc", "source_origin_dt_reloc", "source_err_rms_s_reloc",
    "remarks_reloc", "network_code", "station_code", "station_lat",
    "station_lon", "station_elev_m", "p_arrival_dt", "s_arrival_dt",
    "coda_dt", "magnitude"
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
        "source_id",
        "source_lat_reloc", "source_lon_reloc", "location_reloc", "source_depth_m_reloc", 
        "source_origin_dt_reloc",  "source_err_rms_s_reloc", 
        "source_lat_init", "source_lon_init", "location_init", "source_depth_m_init",
        "source_origin_dt_init",  "source_err_rms_s_init",
        "magnitude"]].drop_duplicates(subset='source_id')
    
    picking_df = df[[
        "source_id", "network_code", "station_code", 
        "station_lat", "station_lon", "station_elev_m",
        "p_arrival_dt", "s_arrival_dt", "coda_dt"
    ]]

    # calculate Ts_Tp for Wadati Profile calculation
    picking_df = picking_df.copy()
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
    picking_df = picking_df.copy()
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


    ## Hypocenter and Station Plots
    # get station data
    station_df = picking_df[picking_df['station_code'].isin(stations)][[
        "station_code", "station_lat", "station_lon", "station_elev_m"
        ]]
    
    hypocenter = {
        'reloc': {
            'latitude': hypocenter_df['source_lat_reloc'].tolist(),
            'longitude': hypocenter_df['source_lon_reloc'].tolist(),
            'elev': (-1 * hypocenter_df['source_depth_m_reloc']).tolist()
        },
        'initial': {
            'latitude': hypocenter_df['source_lat_init'].tolist(),
            'longitude': hypocenter_df['source_lon_init'].tolist(),
            'elev': (-1 * hypocenter_df['source_depth_m_init']).tolist()
        },
        'station': {
            'station_code': station_df['station_code'].tolist(),
            'latitude': station_df['station_lat'].tolist(),
            'longitude': station_df['station_lon'].tolist(),
            'elev': station_df['station_elev_m'].tolist()
        }
    }

    ## RMS error 
    # create histogram data for both reloc and init hypocenter
    bin_width = 0.01
    bin_edges = np.arange(0, (0.1 + bin_width), bin_width)
    hist_rms = {}
    for error_type in ['reloc', 'init']:
        rms_data =  hypocenter_df[f'source_err_rms_s_{error_type}']
        hist_counts, _ = np.histogram(rms_data, bins=bin_edges)
        hist_rms[error_type] = hist_counts.tolist()
    
    hist_rms['bin_width'] = bin_width
    hist_rms['bin_edges'] = bin_edges.tolist()

    ## Magnitude
    magnitude_histogram = {
        'magnitude': hypocenter_df['magnitude'].tolist()
    }


    ## Gutenberg-richter Analysis
    def _gutenberg_analysis(magnitude: pd.Series, min_magnitude, bin_width):

        # drop nan value from magnitude
        valid_magnitude = magnitude.dropna()

        # filtered magnitude
        filtered_magnitudes = valid_magnitude[valid_magnitude >= min_magnitude]

        # Calculate Max Magnitude
        max_magnitude = np.ceil(filtered_magnitudes.max() / bin_width) * bin_width

        # set the magnitude bins
        mag_bins = np.arange(min_magnitude, (max_magnitude + bin_width), bin_width)

        # Cumulative counts 
        cumulative_counts = np.array([len(filtered_magnitudes[filtered_magnitudes >= m]) for m in mag_bins])

        # Non cumulative counts 
        non_cumulative_counts, _ = np.histogram(filtered_magnitudes, bins=mag_bins)

        # Shift the non-cumulative bins to represent bin centers
        mag_bins_non_cum = mag_bins[:-1] + bin_width/2

        # filter out zero counts to avoid log issues
        valid_count_indices_cum = [i for i, c in enumerate(cumulative_counts) if c > 0]
        valid_count_indices_non_cum = [i for i, c in enumerate(non_cumulative_counts) if c > 0]

        if len(valid_count_indices_cum) < 5:
            gutenberg_richter = {}
            return gutenberg_richter

        # Cumulative fit data
        mag_bins_cum = mag_bins[valid_count_indices_cum]
        cumulative_counts = cumulative_counts[valid_count_indices_cum]
        log_cumulative_counts = np.log10(cumulative_counts)

        # Non cumulative data
        mag_bins_non_cum = mag_bins_non_cum[valid_count_indices_non_cum]
        non_cumulative_counts = non_cumulative_counts[valid_count_indices_non_cum]
        log_non_cumulative_counts = np.log10(non_cumulative_counts)

        # fitting to determine b-value, a-value, and magnitude completeness
        # parameter holder
        best_r_squared = 0
        best_breakpoint = mag_bins_cum[0]
        best_slope = 0
        best_intercept = 0
        best_index = 0
        best_std_err = 0

        for i in range( 1, len(mag_bins_cum)//2):
            breakpoint = mag_bins_cum[i]
            mask = mag_bins_cum >= breakpoint
            x_subset = mag_bins_cum[mask]
            y_subset = log_cumulative_counts[mask]

            if len(x_subset) < 2 :
                continue

            slope, intercept, r_value, _, std_err = linregress(x_subset, y_subset)
            r_squared = r_value ** 2

            if r_squared > best_r_squared:
                best_r_squared = r_squared
                best_breakpoint = breakpoint
                best_slope = slope
                best_intercept = intercept
                best_index = i
                best_std_err = std_err
        
        # fitted line 
        fit_log_cumulative = (best_slope * mag_bins_cum) + best_intercept
        mc = (best_breakpoint, fit_log_cumulative[best_index])
        b_value = -1 * best_slope
        a_value = best_intercept
        stderr = best_std_err
        r_value = best_r_squared

        gutenberg_richter = {
            'b_value': b_value,
            'a_value': a_value,
            'b_value_stderr': stderr,
            'r_squared': r_value ** 2,
            'mc': mc,
            'cumulative': {
                'x': mag_bins_cum,
                'y': log_cumulative_counts
            },
            'non_cumulative': {
                'x': mag_bins_non_cum,
                'y': log_non_cumulative_counts
            },
            'fitted_line': {
                'x': mag_bins_cum,
                'y': fit_log_cumulative
            }
        }

        return gutenberg_richter
    
    # call the helper function
    min_magnitude = -2
    guten_bin_width = 0.1
    gutenberg_result = _gutenberg_analysis(min_magnitude=min_magnitude, bin_width=guten_bin_width)    

    # create result objects
    result  = {
        'general_statistics': general_statistics,
        'overall_daily_intensities': overall_daily_intensities,
        'station_performance': station_performance,
        'wadati_profile': wadati_data,
        'time_series_performance': time_series_performance,
        'hypocenter': hypocenter,
        'rms_error': hist_rms,
        'magnitude_histogram': magnitude_histogram,
        'gutenberg_richter': gutenberg_richter
    }

    return result

