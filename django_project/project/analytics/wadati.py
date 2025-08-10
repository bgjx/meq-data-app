import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict

def compute_wadati_profile(picking_df: pd.DataFrame) -> Dict[str, list]:
    """
    Computes the Wadati profile for a given DataFrame containing seismic phase picking information.

    The function calculates the origin time for each unique source_id based on the arrival times 
    of seismic phases and their respective Ts and Tp values. It uses a linear fit to determine the 
    origin time and calculates the P-wave travel times.

    Args:
        picking_df (pd.DataFrame): A DataFrame containing the following columns:
            - source_id (str): Unique identifier for each seismic source.
            - p_arrival_dt (datetime): Arrival dates and times of seismic phases.
            - Ts_Tp (float): Values associated with the phase arrivals used for calculations.

    Returns:
        Dict[str, list]: A dictionary containing:
            - 'p_travel' (list): List of calculated P-wave travel times for each phase.
            - 'ts_tp' (list): List of Ts_Tp values corresponding to the computed travel times.
        """
    epoch = datetime(1970, 1, 1)

    origin_time = {
        'source_id': [],
        'origin_time': []
    }

    for sid in picking_df['source_id'].unique():
        phase_df = picking_df[picking_df['source_id'] == sid].copy()
        phase_df['epoch_delta'] = phase_df['p_arrival_dt'].apply(
            lambda x: (x - epoch).total_seconds()
        )

        # calculate the t_0 with np.polyfit
        z = np.polyfit(phase_df['epoch_delta'], phase_df['Ts_Tp'], 1)
        t_0 = (-1 * z[1]) / z[0]
        t_0_dt = epoch + timedelta(seconds=t_0)

        origin_time['source_id'].append(sid)
        origin_time['origin_time'].append(t_0_dt)
    
    origin_time_df = pd.DataFrame.from_dict(origin_time)
    merged = picking_df.merge(
        origin_time_df,
        on='source_id',
        how='inner'
    )
    merged['p_travel'] = (merged['p_arrival_dt'] - merged['origin_time']).dt.total_seconds()

    return {
        'p_travel': merged['p_travel'].tolist(),
        'ts_tp': merged['Ts_Tp'].tolist()
    }
