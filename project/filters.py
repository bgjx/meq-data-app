import django_filters
from django import forms
from django_filters import DateFilter, NumberFilter
from django.apps import apps
from django.db.models import Min, Max

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import point
from django.contrib.gis.measure import D

import numpy as np


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
    picked_model = apps.get_model('projects', model_name)

    # get the data time scope
    min_date = picked_model.objects.all().aggregate(min_date=Min('source_origin_dt'))['min_date']
    max_date = picked_model.objects.all().aggregate(max_date=Max('source_origin_dt'))['max_date']

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
        
        # Circular Radius Filter Fields
        latitude = NumberFilter(
            label = "Center Latitude",
            widget = forms.NumberInput(
                attrs={
                    'placeholder': f'latitude: {median_lat}',
                    'step': 'any'
                }
            )
        )

        longitude = NumberFilter(
            label= "Center Longitude",
            widget = forms.NumberInput(
                attrs={
                    'placeholder': f'longitude: {median_lon}',
                    'step': 'any'
                }
            )
        )

        radius = NumberFilter(
            label='Radius (Km)',
            widget = forms.NumberInput(
                attrs={
                    'placeholder': 'Radius in kilometers',
                    'min': '0',
                    'step':'any'
                }
            )
        )

        class Meta:
            model = picked_model
            fields = ['start_date', 'end_date', 'latitude', 'longitude', 'radius']
    
    return SpatialFilter


def slider_filter(model_name):
    picked_model = apps.get_model('project', model_name)

    # Get the min and max years from 






