from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Min , Max

from project.analytics.services import (
    analyze_general_performance,
    analyze_detail_analytics
)

from project.utils import get_merged_catalog, get_filtered_queryset


class HypocenterTableAPIView(APIView):
    """
    API endpoints to fetch hypocenter table of microearthquake monitoring.
    """
    def get(self, request, catalog_type:str, site_slug:str = None) -> HttpResponse:



class GeneralPerformanceAPIView(APIView):
    """
    API endpoints to fetch general performance of microearthquake monitoring.
    """
    def get(self, request, site_slug=None):
        model = get_merged_catalog('project', site_slug)
        if not model:
            Response({"error": "Requested catalog not found"}, status=status.HTTP_404_NOT_FOUND)

        queryset = get_filtered_queryset(model, request.GET)

        try:
            data = analyze_general_performance(queryset, site_slug)
        except ValueError as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data["time_range"] = {
            "site": str.upper(site_slug),
            "min_datetime" : queryset.aggregate(Min("source_origin_dt_init"))["source_origin_dt_init__min"],
            "max_datetime" : queryset.aggregate(Max("source_origin_dt_init"))["source_origin_dt_init__max"]
        }
        
        return Response(data, status=status.HTTP_200_OK)


class DetailAnalyticsAPIView(APIView):
    """
    API endpoints to fetch detail analytics of microearthquake monitoring.
    """
    def get(self, request, site_slug=None):
        model = get_merged_catalog('project', site_slug)
        if not model:
            return Response({"error": "Requested catalog not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = get_filtered_queryset(model, request.GET)

        try:
            data = analyze_detail_analytics(queryset, site_slug)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        data["time_range"] = {
            "site": str.upper(site_slug),
            "min_datetime" : queryset.aggregate(Min("source_origin_dt_init"))["source_origin_dt_init__min"],
            "max_datetime" : queryset.aggregate(Max("source_origin_dt_init"))["source_origin_dt_init__max"]
        }

        return Response(data, status=status.HTTP_200_OK)




