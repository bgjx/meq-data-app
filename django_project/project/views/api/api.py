from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.apps import apps

import pandas as pd

from project.filters import spatial_filter
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
from project.utils import get_merged_catalog


class GeneralPerformanceAPIView(APIView):
    """
    API endpoints to fetch general performance of microearthquake monitoring.
    """
    def get(self, request, site_slug=None):
        model = get_merged_catalog('project', site_slug)
        get_model = apps.get_model('project', model)

        filter_class = spatial_filter(model)
        filter_instance = filter_class(request.GET, queryset=get_model.objects.all())
        queryset = filter_instance.qs 

        df = pd.DataFrame.from_records(queryset.values())

        validated_df = validate_dataframe(df)

        if not validated_df:
            return Response({}, status=status.HTTP_200_OK)

        hypocenter_df, picking_df = preprocess_dataframe(validated_df)

        data = {
            'general_statistic': compute_general_statistics(hypocenter_df, picking_df),
            'overall_daily_intensities': compute_overall_daily_intensities(picking_df),
            'hypocenter': retrieve_catalog_hypocenter(hypocenter_df, picking_df, site_slug)
        }

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class DetailAnalyticsAPIView(APIView):
    """
    API endpoints to fetch detail analytics of microearthquake monitoring.
    """
    def get(self, request, site_slug=None):
        model = get_merged_catalog('project', site_slug)
        get_model = apps.get_model('project', model)

        filter_class = spatial_filter(model)
        filter_instance = filter_class(request.GET, queryset=get_model.objects.all())
        queryset = filter_instance.qs

        df = pd.DataFrame.from_records(queryset.values())

        validated_df = validate_dataframe(df)

        if not validated_df:
            return Response({}, status=status.HTTP_200_OK)
        
        hypocenter_df, picking_df = preprocess_dataframe(validated_df)
        magnitude_series = hypocenter_df['magnitude'].dropna()

        data = {
            'time_series_performance': compute_time_series_performance(picking_df),
            'station_performance': compute_station_performance(picking_df),
            'wadati_profile': compute_wadati_profile(picking_df),
            'hypocenter': retrieve_catalog_hypocenter(hypocenter_df, picking_df, site_slug),
            'gap_histogram': {'gap': hypocenter_df['gap_init'].dropna().tolist()},
            'rms_error': compute_hypocenter_rms_error(hypocenter_df),
            'magnitude_histogram': {'magnitude':magnitude_series.tolist()},
            'gutenberg_analysis': gutenberg_analysis(magnitude_series)
        }

        return Response(data, status=status.HTTP_200_OK)




