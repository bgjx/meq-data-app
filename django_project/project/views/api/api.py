from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Min , Max

from project.analytics.services import (
    analyze_general_performance,
    analyze_detail_analytics
)

from project.utils import (
    get_hypocenter_catalog,
    get_picking_catalog,
    get_station,
    get_merged_catalog,
    get_filtered_queryset
)

class HypocenterTableAPIView(APIView):
    """
    API endpoints to fetch hypocenter data for table UI.
    """
    def get(self, request, catalog_type:str, site_slug:str = None) -> HttpResponse:
        model = get_hypocenter_catalog('project', site_slug, catalog_type)
        if not model:
            Response({"error": "Requested data not found"}, status = status.HTTP_404_NOT_FOUND)
    
        queryset = get_filtered_queryset(model, request.GET, 'hypocenter_table_filter')

        # serialize data
        data = [
            {
                "source_id": obj.source_id,
                "source_lat": obj.source_lat,
                "source_lon": obj.source_lon,
                "source_depth_m": obj.source_depth_m,
                "source_origin_dt": obj.source_origin_dt,
                "source_err_rms_s": obj.source_err_rms_s,
                "magnitude": obj.magnitude,
                "remarks": obj.remarks
            } for obj in queryset
        ]

        return Response({"data":data}, status=status.HTTP_200_OK)


class PickingTableAPIView(APIView):
    """
    API endpoints to fetch picking data for table UI.
    """
    def get(self, request, catalog_type:str, site_slug:str=None) -> HttpResponse:
        model = get_picking_catalog('project', site_slug)
        if not model:
            Response({"error": "Requested data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = get_filtered_queryset(model, request.GET, 'picking_table_filter')

        # serialize data 
        data = [
            {
                "source_id": obj.source_id,
                "station_code": obj.station_code,
                "p_arrival_dt": obj.p_arrival_dt,
                "p_polarity": obj.p_polarity,
                "p_onset": obj.p_onset,
                "s_arrival_dt": obj.s_arrival_dt,
                "coda_dt": obj.coda_dt
            } for obj in queryset
        ]

        return Response({"data":data}, status=status.HTTP_200_OK)


class StationTableAPIView(APIView):
    """
    API endpoints to fetch station data for table UI.
    """
    def get(self, request, catalog_type: str, site_slug:str=None) -> HttpResponse:
        model = get_station('project', site_slug)
        if not model:
            Response({"error":"Requested data not found"}, status=status.HTTP_404_NOT_FOUND)

        queryset = model.objects.all()

        # serialize data
        data = [
            {
                "station_code": obj.station_code,
                "network_code": obj.network_code,
                "station_lat": obj.station_lat,
                "station_lon": obj.station_lon,
                "station_elev_m": obj.station_elev_m
            } for obj in queryset
        ]

        return Response({"data":data}, status=status.HTTP_200_OK)


class GeneralPerformanceAPIView(APIView):
    """
    API endpoints to fetch general performance of microearthquake monitoring.
    """
    def get(self, request, site_slug=None):
        model = get_merged_catalog('project', site_slug)
        if not model:
            Response({"error": "Requested catalog not found"}, status=status.HTTP_404_NOT_FOUND)

        queryset = get_filtered_queryset(model, request.GET, 'spatial_filter')

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
        
        queryset = get_filtered_queryset(model, request.GET, 'spatial_filter')

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




