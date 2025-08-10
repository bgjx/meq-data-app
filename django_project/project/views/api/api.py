from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from analytics.base import validate_dataframe, preprocess_dataframe
from analytics.general import (
    compute_general_statistics,
    compute_overall_daily_intensities,
    compute_station_performance,
    compute_time_series_performance,
    retrieve_catalog_hypocenter
)
from analytics.wadati import compute_wadati_profile
from analytics.gutenberg import gutenberg_analysis