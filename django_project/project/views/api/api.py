from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from project.views.api.pagination import DataTablesPagination

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

class HypocenterTableDataAPIView(APIView):
    """
    API endpoints to fetch hypocenter data for table UI.
    """

    pagination_class = DataTablesPagination

    def get(self, request, catalog_type:str, site_slug:str = None) -> HttpResponse:
        model = get_hypocenter_catalog('project', site_slug, catalog_type)
        if not model:
            Response({"error": "Requested data not found"}, status = status.HTTP_404_NOT_FOUND)

        # high-level filter
        queryset = get_filtered_queryset(model, request.GET, 'hypocenter_table_filter')

        # Global search from DataTables
        search_value = request.GET.get('search[value]', '').strip()
        if search_value:
            queryset = queryset.filter(
                Q(source_id__icontains=search_value) |
                Q(source_lat__icontains=search_value) |
                Q(source_lon__icontains=search_value) |
                Q(source_depth_m__icontains=search_value) |
                Q(magnitude__icontains=search_value) |
                Q(remarks__icontains=search_value)
            )
        
        # ordering from DataTables
        order_column_index = request.GET.get('order[0][column]')
        order_dir = request.GET.get('order[0][dir]', 'asc')
        columns = [
            'source_id', 'source_lat', 'source_lon', 'source_depth_m',
            'source_origin_dt', 'magnitude', 'remarks'
        ]

        if order_column_index and order_column_index.isdigit():
            order_field = columns[int(order_column_index)]
            if order_dir == 'desc':
                order_field = '-' + order_field
            queryset = queryset.order_by(order_field)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        # serialize data
        data = [
            {
                "source_id": obj.source_id,
                "source_lat": obj.source_lat,
                "source_lon": obj.source_lon,
                "source_depth_m": obj.source_depth_m,
                "source_origin_dt": obj.source_origin_dt,
                "magnitude": obj.magnitude,
                "remarks": obj.remarks
            } for obj in page
        ]

        return paginator.get_paginated_response(data)
    

class PickingTableDataAPIView(APIView):
    """
    API endpoints to fetch picking data for table UI.
    """

    pagination_class = DataTablesPagination

    def get(self, request, site_slug:str = None) -> HttpResponse:
        model = get_picking_catalog('project', site_slug)
        if not model:
            Response({"error": "Requested data not found"}, status = status.HTTP_404_NOT_FOUND)

        # high-level filter
        queryset = get_filtered_queryset(model, request.GET, 'picking_table_filter')

        # Global search from DataTables
        search_value = request.GET.get('search[value]', '').strip()
        if search_value:
            queryset = queryset.filter(
                Q(source_id__icontains=search_value) |
                Q(station_code__icontains=search_value)
            )
        
        # ordering from DataTables
        order_column_index = request.GET.get('order[0][column]')
        order_dir = request.GET.get('order[0][dir]', 'asc')
        columns = [
            'source_id', 'station_code', 'p_arrival_dt', 'p_polarity',
            'p_onset', 's_arrival_dt', 'coda_dt'
        ]

        if order_column_index and order_column_index.isdigit():
            order_field = columns[int(order_column_index)]
            if order_dir == 'desc':
                order_field = '-' + order_field
            queryset = queryset.order_by(order_field)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

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
            } for obj in page
        ]

        return paginator.get_paginated_response(data)


class StationTableDataAPIView(APIView):
    """
    API endpoints to fetch station data for table UI.
    """
    def get(self, request, site_slug:str=None) -> HttpResponse:
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




