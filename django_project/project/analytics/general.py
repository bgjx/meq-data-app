import numpy as np
import pandas as pd
from typing import Dict


def compute_general_statistics(

    hypocenter_df: pd.DataFrame,
    picking_df: pd.DataFrame
    ) -> Dict[str, int]:
    
    """
    Compute general statistics from hypocenter and picking data.

    Args:
      hypocenter_df (pd.DataFrame): DataFrame containing hypocenter information.
      picking_df (pd.DataFrame): DataFrame containing picking information.

    Returns:
      Dict[str, int]: A dictionary containing total events, total phases, and total stations.
    """
    source_id = hypocenter_df['source_id'].unique()
    stations = sorted(picking_df['station_code'].unique())

    return {
        'total_events': len(hypocenter_df['source_id']),
        'total_phases': len(picking_df['p_arrival_dt']) + len(picking_df['s_arrival_dt']),
        'total_stations': len(stations)
    }


def compute_overall_daily_intensities(hypocenter_df: pd.DataFrame) -> Dict[str, list]:
    """
    Compute overall daily intensities from hypocenter data.

    Args:
      hypocenter_df (pd.DataFrame): DataFrame containing hypocenter information.

    Returns:
      Dict[str, list]: A dictionary with x values (dates), y_bar (daily counts), and y_cum (cumulative counts).
    """
    date_series = pd.to_datetime(hypocenter_df['source_origin_dt_init'])
    grouped_daily_data = date_series.groupby(
        [
            date_series.dt.year,
            date_series.dt.month,
            date_series.dt.day
        ]
    ).size()

    x_values = [f"{year}-{month:02d}-{day:02d}" for year, month, day in grouped_daily_data.index]
    y_array = grouped_daily_data.values

    return {
        'x_values': x_values,
        'y_bar': y_array.tolist(),
        'y_cum': np.cumsum(y_array).tolist()
    }


def compute_station_performance(picking_df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
    """
    Compute performance metrics for each station from picking data.

    Args:
      picking_df (pd.DataFrame): DataFrame containing picking information.

    Returns:
    Dict[str, Dict[str, int]]: A dictionary where each key is a station code and each value is another dictionary
                                with counts of P and S phases.
    """
    station_performance = {}

    for sta in sorted(picking_df['station_code'].unique()):
        phases = picking_df[picking_df['station_code'] == sta]
        station_performance[sta] = {
            'p_phase': len(phases['p_arrival_dt']),
            's_phase': len(phases['s_arrival_dt'])
        }
    
    return station_performance


def compute_time_series_performance(picking_df: pd.DataFrame) -> Dict[str, list]:
    """
    Compute time series performance metrics from picking data.

    Args:
        picking_df (pd.DataFrame): DataFrame containing picking information.

    Returns:
        Dict[str, list]: A dictionary containing dates, station codes, and counts as lists.
    """
    picking_df = picking_df.copy()
    picking_df['p_arrival_dt_date'] = pd.to_datetime(picking_df['p_arrival_dt']).dt.date

    pivot_station = pd.pivot_table(
        picking_df,
        index='p_arrival_dt_date',
        columns='station_code',
        aggfunc='size',
        fill_value=0
    )

    pivot_station.index = [f"{index.year}-{index.month:02d}-{index.day:02d}" for index in pivot_station.index]

    return {
        'dates': pivot_station.index.tolist(),
        'stations': pivot_station.columns.tolist(),
        'counts': pivot_station.to_dict('index')
    }
