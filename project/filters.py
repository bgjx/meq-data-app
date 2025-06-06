import django_filters
from django import forms
from django_filters import DateFilter, NumberFilter
from django.apps import apps
from django.db.models import Min, Max

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

import numpy as np
import logging

logger = logging.getLogger(__name__)


def table_filter(model_name):
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

    # get the data time scope
    min_date = picked_model.objects.all().aggregate(min_date=Min('source_origin_dt_init'))['min_date']
    max_date = picked_model.objects.all().aggregate(max_date=Max('source_origin_dt_init'))['max_date']

    # get the data spacial scope by calculating the median
    lat_lon = picked_model.objects.values('source_id', 'source_lat_init', 'source_lon_init').distinct()
    if lat_lon:
        latitudes = [ loc['source_lat_init'] for loc in lat_lon]
        longitudes = [loc['source_lon_init'] for loc in lat_lon]
        median_lat = np.median(latitudes) if latitudes else 0
        median_lon = np.median(longitudes) if longitudes else 0
    else:
        median_lat, median_lon = 0, 0
    

    class SpatialFilter(django_filters.FilterSet):
        # Date Range Filters
        start_date = DateFilter(field_name="source_origin_dt_init", 
                                lookup_expr="gte", 
                                label="Start Date",
                                # widget = forms.DateInput(
                                #     attrs={
                                #         'type': 'text',
                                #         'min': min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else '',
                                #         'max': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else '',
                                #         'placeholder':  min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else ''
                                #     }
                                # )
                    )
        
        end_date = DateFilter(field_name="source_origin_dt_init",
                              lookup_expr="lte", 
                              label="End Date",
                            #   widget = forms.DateInput(
                            #       attrs={
                            #             'type': 'text',
                            #             'min': min_date.strftime('%Y-%m-%d %H:%M:%S') if min_date else '',
                            #             'max': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else '',
                            #             'placeholder': max_date.strftime('%Y-%m-%d %H:%M:%S') if max_date else ''
                            #       }
                            #   )
                    )
        
        # Circular Radius Filter Fields
        latitude = NumberFilter(
            label = "Center Latitude",
            # widget = forms.NumberInput(
            #     attrs={
            #         'placeholder': f'latitude: {median_lat}',
            #         'min': -90,
            #         'max': 90,
            #         'step': 'any'
            #     }
            # )
        )

        longitude = NumberFilter(
            label= "Center Longitude",
            # widget = forms.NumberInput(
            #     attrs={
            #         'placeholder': f'longitude: {median_lon}',
            #         'min': -180,
            #         'max': 180,
            #         'step': 'any'
            #     }
            # )
        )

        radius = NumberFilter(
            label='Radius (Km)',
            # widget = forms.NumberInput(
            #     attrs={
            #         'placeholder': 'Radius in kilometers',
            #         'min': 0,
            #         'step':'any'
            #     }
            # )
        )

        class Meta:
            model = picked_model
            fields = ['start_date', 'end_date', 'latitude', 'longitude', 'radius']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.filters['latitude'].required = False
            self.filters['longitude'].required = False
            self.filters['radius'].required = False
        
        def filter_queryset(self, queryset):
            queryset =  super().filter_queryset(queryset)

            latitude = self.form.cleaned_data.get('latitude')
            longitude = self.form.cleaned_data.get('longitude')
            radius = self.form.cleaned_data.get('radius')
        
            if all (v is not None for v in [latitude, longitude, radius]):
                try:
                    # validate form filter input
                    if not (-90 <= latitude <=90 ):
                        logger.error(f"Invalid latitude: {latitude}")
                        return queryset
                    if not(-180 <= longitude <=180):
                        logger.error(f"Invalid longitude: {longitude}")
                    if radius < 0:
                        logger.error(f"Invalid radius: {radius}")
                        return queryset
                    
                    # create central point for reference
                    center_point = Point(longitude, latitude, srid=4326)

                    queryset = queryset.filter(
                        location_init_isnull = False
                        ).filter(
                            location_init_dwithin = (center_point, D(km=radius))
                        ).annotate(
                            distance = Distance('location_init', center_point)
                        )

                except Exception as e:
                    logger.error(f"Spatial filter error: {str(e)}")
            return queryset
        
    return SpatialFilter


def slider_filter(model_name):
    picked_model = apps.get_model('project', model_name)

    # Get the min and max years from 






