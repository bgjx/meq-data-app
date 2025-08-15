import pandas as pd

from typing import Dict, List, Tuple

from project.analytics.base import validate_dataframe, preprocess_dataframe
from project.analytics.general import (
    compute_general_statistics,
    compute_overall_daily_intensities,
    compute_station_performance,
    compute_time_series_performance,
    retrieve_catalog_hypocenter,
    compute_hypocenter_rms_error
)
from project.analytics.wadati import compute_wadati_profile
from project.analytics.gutenberg import gutenberg_analysis


def analyze_general_performance(queryset, site_slug:str) -> Dict[str, Dict[str, list]]:

    df = pd.DataFrame.from_records(queryset.values())
    validate_dataframe(df)
    hypocenter_df, picking_df = preprocess_dataframe(df)

    return {
        'general_statistics': compute_general_statistics(hypocenter_df, picking_df),
        'overall_daily_intensities': compute_overall_daily_intensities(hypocenter_df),
        'hypocenter': retrieve_catalog_hypocenter(hypocenter_df, picking_df, site_slug)
        }


def analyze_detail_analytics(queryset, site_slug:str) -> Dict[str, Dict[str, list]]:

    df = pd.DataFrame.from_records(queryset.values())
    validate_dataframe(df)

    hypocenter_df, picking_df = preprocess_dataframe(df)
    magnitude_series = hypocenter_df['magnitude'].dropna()

    return {
        'time_series_performance': compute_time_series_performance(picking_df),
        'station_performance': compute_station_performance(picking_df),
        'wadati_profile': compute_wadati_profile(picking_df),
        'hypocenter': retrieve_catalog_hypocenter(hypocenter_df, picking_df, site_slug),
        'gap_histogram': {'gap': hypocenter_df['gap_init'].dropna().tolist()},
        'rms_error': compute_hypocenter_rms_error(hypocenter_df),
        'magnitude_histogram': {'magnitude':magnitude_series.tolist()},
        'gutenberg_analysis': gutenberg_analysis(magnitude_series)
        }
