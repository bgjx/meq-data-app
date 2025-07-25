import django_filters
from django import forms
from django_filters import DateTimeFilter, NumberFilter
from django.apps import apps
from django.db.models import Min, Max

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

import logging


logger = logging.getLogger(__name__)


# filter for hypocenter catalog table
def hypo_table_filter(model_name):
    picked_model = apps.get_model('project', model_name)

    # get the data time scope
    min_date = picked_model.objects.all().aggregate(min_date=Min('source_origin_dt'))['min_date']
    max_date = picked_model.objects.all().aggregate(max_date=Max('source_origin_dt'))['max_date']

    # Inherit django filter class object
    class HypoTableFilter(django_filters.FilterSet):
        hypo_start_date = DateTimeFilter(field_name="source_origin_dt", 
                                lookup_expr="gte", 
                                label="Start Date",
                                widget = forms.DateInput(
                                    attrs={
                                        'type': 'text',
                                        'min': min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else '',
                                        'max': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else '',
                                        'placeholder':  min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else ''
                                    }
                                )
        )
        
        hypo_end_date = DateTimeFilter(field_name="source_origin_dt",
                              lookup_expr="lte", 
                              label="End Date",
                              widget = forms.DateInput(
                                  attrs={
                                        'type': 'text',
                                        'min': min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else '',
                                        'max': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else '',
                                        'placeholder': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else ''
                                  }
                              )
        )
        
        class Meta:
            model = picked_model
            fields = []
    return HypoTableFilter


# filter for picking catalog table
def picking_table_filter(model_name):
    picked_model = apps.get_model('project', model_name)

    # Get the data time scope (base on P-arrival)
    min_date = picked_model.objects.all().aggregate(min_date = Min('p_arrival_dt'))['min_date']
    max_date = picked_model.objects.all().aggregate(max_date = Max('p_arrival_dt'))['max_date']

    # Inherit django filter class object
    class PickTableFilter(django_filters.FilterSet):
        picking_start_date = DateTimeFilter( field_name="p_arrival_dt",
                                lookup_expr="gte",
                                label="Start Date",
                                widget = forms.DateInput(
                                    attrs={
                                        'type': 'text',
                                        'min': min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else '',
                                        'max': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else '',
                                        'placeholder':  min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else ''
                                    },
                                ),
        )

        picking_end_date = DateTimeFilter(field_name= "p_arrival_dt",
                              lookup_expr="lte",
                              label="End Date",
                              widget = forms.DateInput(
                                  attrs={
                                        'type': 'text',
                                        'min': min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else '',
                                        'max': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else '',
                                        'placeholder': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else ''
                                  },
                              ),
        )

        class Meta:
            model = picked_model
            fields = []
    
    return PickTableFilter


# dynamic spatial filter
def spatial_filter(model_name):
    'Spatial filter, differ from table filter it uses view merged catalog in database'
    picked_model = apps.get_model('project', model_name)  

    class SpatialFilter(django_filters.FilterSet):
        # Date Range Filters
        start_date = DateTimeFilter(field_name="source_origin_dt_init", 
                                lookup_expr="gte", 
                                label="Start Date"
                    )
        
        end_date = DateTimeFilter(field_name="source_origin_dt_init",
                              lookup_expr="lte", 
                              label="End Date",
                    )
        
        # Circular Radius Filter Fields
        radius = NumberFilter(
            method='filter_by_radius',
            label='Radius (Km)',
            required=False
        )

        center_latitude = NumberFilter(
            method='noop',
            field_name=None,
            label="Center Latitude",
            required=False
        )

        center_longitude = NumberFilter(
            method='noop',
            field_name=None,
            label="Center Longitude",
            required=False
        )

        # Rectangular Filter fields
        min_latitude = NumberFilter(
            method='noop',
            field_name=None,
            label= "Min Latitude",
            required=False
        )

        max_latitude  = NumberFilter(
            method='noop',
            field_name=None,
            label= "Max Latitude",
            required=False
        )

        min_longitude = NumberFilter(
            method='noop',
            field_name=None,
            label= "Min Longitude",
            required=False
        )

        max_longitude = NumberFilter(
            field_name=None,
            method='filter_by_bbox',
            label= "Max Longitude",
            required=False
        )


        def noop(self, queryset, name, value):
            return queryset
        

        def filter_by_radius(self, queryset, name, value):

            if value is None:
                return queryset
            
            # get filter parameters
            center_latitude = self.data.get('center_latitude')
            center_longitude = self.data.get('center_longitude')
            radius = value

            try:
                center_latitude = float(center_latitude)
                center_longitude = float(center_longitude)
                radius = float(radius)
            except (TypeError, ValueError):
                return queryset

            if not (-90 <= center_latitude <=90 and -180 <= center_longitude <=180 and radius >= 0):
                return queryset
            
            center_point = Point(center_longitude, center_latitude, srid=4326)
            degree_radius = radius / 111.0
            queryset = queryset.filter(
                location_init__isnull = False
                ).filter(
                    location_init__dwithin = (center_point, degree_radius)
                ).annotate(
                    distance = Distance('location_init', center_point)
                )
            
            return queryset
        

        def filter_by_bbox(self, queryset, name, value):

            if value is None:
                return queryset
            
            min_latitude = self.data.get('min_latitude')
            max_latitude = self.data.get('max_latitude')
            min_longitude = self.data.get('min_longitude')
            max_longitude = value

            try:
                min_latitude = float(min_latitude)
                max_latitude = float(max_latitude)
                min_longitude = float(min_longitude)
                max_longitude = float(max_longitude)
            except (TypeError, ValueError):
                return queryset

            if not (-90 <= min_latitude <= max_latitude <= 90 and -180 <= min_longitude <= max_longitude <=180):
                return queryset

            # create polygon for the rectangular bounding box
            bbox = Polygon (
                (
                    (min_longitude, min_latitude),
                    (min_longitude, max_latitude),
                    (max_longitude, max_latitude),
                    (max_longitude, min_latitude),
                    (min_longitude,  min_latitude)
                ),
                srid= 4326
            )
            queryset = queryset.filter(
                location_init__isnull = False
            ).filter(
                location_init__within = bbox
            )

            return queryset
        
        class Meta:
            model = picked_model
            fields = []

    return SpatialFilter




