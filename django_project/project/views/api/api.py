from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.apps import apps

import pandas as pd

from project.filters import spatial_filter

from project.analytics.services import (
    analyze_general_performance,
    analyze_detail_analytics
)

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

        try:
            data = analyze_general_performance(queryset, site_slug)
        except ValueError as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


        return Response(data, status=status.HTTP_200_OK)


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

        try:
            data = analyze_detail_analytics(queryset, site_slug)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)




