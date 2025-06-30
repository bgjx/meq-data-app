import django_filters
from django import forms
from django_filters import DateFilter, NumberFilter
from django.apps import apps
from django.db.models import Min, Max

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

import numpy as np
import logging

logger = logging.getLogger(__name__)


def hypo_table_filter(model_name):
    picked_model = apps.get_model('project', model_name)

    # get the data time scope
    min_date = picked_model.objects.all().aggregate(min_date=Min('source_origin_dt'))['min_date']
    max_date = picked_model.objects.all().aggregate(max_date=Max('source_origin_dt'))['max_date']

    class TableFilter(django_filters.FilterSet):
        start_date = DateFilter(field_name="source_origin_dt", 
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
        
        end_date = DateFilter(field_name="source_origin_dt",
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
    return TableFilter


def spatial_filter(model_name):
    'Spatial filter, differ from table filter it uses view merged catalog in database'
    picked_model = apps.get_model('project', model_name)  

    class SpatialFilter(django_filters.FilterSet):
        # Date Range Filters
        start_date = DateFilter(field_name="source_origin_dt_init", 
                                lookup_expr="gte", 
                                label="Start Date"
                    )
        
        end_date = DateFilter(field_name="source_origin_dt_init",
                              lookup_expr="lte", 
                              label="End Date",
                    )
        
        # Circular Radius Filter Fields
        center_latitude = NumberFilter(
            label = "Center Latitude",
        )

        center_longitude = NumberFilter(
            label= "Center Longitude",
        )

        radius = NumberFilter(
            label='Radius (Km)',
        )

        # Rectangular Filter fields
        min_latitude = NumberFilter(
            label= "Min Latitude"
        )

        max_latitude  = NumberFilter(
            label = "Max Latitude"
        )

        min_longitude = NumberFilter(
            label= "Min Longitude"
        )

        max_longitude = NumberFilter(
            label= "Max Longitude"
        )


        class Meta:
            model = picked_model
            fields = ['start_date', 'end_date',
                    'center_latitude', 'center_longitude', 'radius',
                    'min_latitude', 'max_latitude', 'min_longitude', 'max_longitude']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Rectangular filter require status
            self.filters['min_latitude'].required = False
            self.filters['max_latitude'].required = False 
            self.filters['min_longitude'].required = False 
            self.filters['max_longitude'].required = False

            # Circular filter require status
            self.filters['center_latitude'].required = False
            self.filters['center_longitude'].required = False
            self.filters['radius'].required = False
        
        def filter_queryset(self, queryset):
            # Apply base filter before areal filter first
            queryset =  super().filter_queryset(queryset)

            # clean rectangular filter form parameters
            min_latitude = self.form.cleaned_data.get('min_latitude')
            max_latitude = self.form.cleaned_data.get('max_latitude')
            min_longitude = self.form.cleaned_data.get('min_longitude')
            max_longitude = self.form.cleaned_data.get('max_longitude')

            # clean circular filter form parameters
            center_latitude = self.form.cleaned_data.get('center_latitude')
            center_longitude = self.form.cleaned_data.get('center_longitude')
            radius = self.form.cleaned_data.get('radius')


            try:
                if all (v is not None for v in [center_latitude, center_longitude, radius]):
                    # validate form filter input
                    if not (-90 <= center_latitude <=90 ):
                        logger.error(f"Invalid latitude: {center_latitude}")
                        return queryset
                    if not(-180 <= center_longitude <=180):
                        logger.error(f"Invalid longitude: {center_longitude}")
                    if radius < 0:
                        logger.error(f"Invalid radius: {radius}")
                        return queryset
                    
                    # create central point for reference
                    center_point = Point(center_longitude, center_latitude, srid=4326)
                    queryset = queryset.filter(
                        location_init_isnull = False
                        ).filter(
                            location_init_dwithin = (center_point, D(km=radius))
                        ).annotate(
                            distance = Distance('location_init', center_point)
                        )
                
                # Apply rectangular filter if the circular filter is not used.
                elif all ( v is not None for v in [min_latitude, max_latitude, min_longitude, max_longitude]):
                    if not (-90 <= min_latitude <= max_latitude <= 90):
                        logger.error(f"Invalid latitude range: min={min_latitude}, max={max_latitude}")
                        return queryset
                    if not (-180 <= min_longitude <= max_longitude <=180):
                        logger.error(f"Invalid longitude range: min={min_longitude}, max={max_longitude}")
                        return queryset

                    # create polygon for the rectangular bounding box
                    bbox = Polygon (
                        (
                            (min_longitude, min_latitude),
                            (max_longitude, min_latitude),
                            (max_longitude, max_latitude),
                            (max_longitude, min_latitude),
                            (min_longitude,  min_latitude)
                        ),
                        srid= 4326
                    )
                    queryset = queryset.filter(
                        location_init_isnull = False
                    ).filter(
                        location_init_within = bbox
                    )
            except Exception as e :
                logger.error(f"Spatial filter error: {str(e)}")
                return queryset
            
            return queryset
        
    return SpatialFilter





