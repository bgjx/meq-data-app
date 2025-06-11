from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from django.conf import settings

from frontpage.models import Site
from project.utils import (get_hypocenter_catalog, 
                           get_station,
                           get_merged_catalog,
                           analysis_engine)
from . filters import table_filter, spatial_filter

from datetime import datetime, timedelta
import pandas as pd
import csv

# Function for page view renderer
def project_site(request, site_slug = None):
    'View function for data explorer page.'
    site = get_object_or_404(Site, slug=site_slug)

    # Define catalog types and their download URLs
    catalog_types = [
        {'type': 'relocated', 'download_url':'download-relocated'},
        {'type': 'initial', 'download_url': 'download-initial'}
    ]

    #  Process each catalog
    context = {'site': site}
    for catalog in catalog_types:
        catalog_type = catalog['type']
        # Get model
        db_table, model = get_hypocenter_catalog('project', site_slug, catalog_type)
        # apply filter
        filter_class = table_filter(model)
        filter_instance = filter_class(request.GET, queryset=db_table)
        # update context
        context[f'table_{catalog_type}'] = filter_instance.qs
        context[f'date_filter_{catalog_type}'] = filter_instance

    return render(request, 'project/data-explore.html', context)


def meq_maps(request, site_slug = None):
    'Generate map frame for meq distributions map'
    site = get_object_or_404(Site, slug=site_slug)
    mapbox_access_token = settings.MAPBOX_API_TOKEN
    context = {
        'site': site,
        'MAPBOX_TOKEN': mapbox_access_token,
    }
    return render(request, 'project/event-distributions.html', context=context)


def data_analysis(request, site_slug = None):
    'Generate views for data analysis page.'
    site = get_object_or_404(Site, slug=site_slug)

    # get current datetime
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    w_before = now - timedelta(days=7)
    w_before_str = w_before.strftime("%Y-%m-%d %H:%M:%S") 


    context = {
                'site': site,
                'now_time': now_str,
                'week_before_time': w_before_str
    }
    
    return render(request, 'project/data-analysis.html', context)


#  API endpoint function
def get_meq_data(request, site_slug = None):
    'API endpoint to get hypocenter data and calculate the center point'

    site = get_object_or_404(Site, slug=site_slug)    
    # map center
    center_map = {
        'seml': {'lat': -1.616487, 'lon':101.137171},
        'serd': {'lat': -4.220185, 'lon': 103.379187}
    }

    # define catalog type
    catalog_types = [
        {'type': 'relocated'},
        {'type': 'initial'}
    ]
    
    # get station dataframe
    db_station = get_station('project', site_slug)
    df_station = pd.DataFrame(list(db_station.values()))

    data = {
        'station': df_station.to_dict(orient='records'),
        'center_map': center_map[site_slug]
    }

    # get hypocenter dataframe and normalize magnitude 
    for catalog in catalog_types:
        catalog_type = catalog['type']
        db_table, model = get_hypocenter_catalog('project', site_slug, catalog_type)
        df_meq = pd.DataFrame(list(db_table.values()))
        df_meq = df_meq[['source_id', 'source_lat', 'source_lon', 'source_depth_m', 'magnitude']]
        
        # magnitude normalization
        average_magnitude = df_meq.magnitude.median()
        df_meq['magnitude'] = df_meq['magnitude'].fillna(average_magnitude)

        min_magnitude = df_meq.magnitude.min()
        normalized_magnitude = [1 * (( -1 * min_magnitude) + data) for data in list(df_meq.magnitude)]
        df_meq['norm_magnitude'] = normalized_magnitude

        # update data object
        data[f'meq_{catalog_type}'] = df_meq.to_dict(orient='records')

    return JsonResponse(data)


def get_analysis_data( request, site_slug=None):
    'API endpoint to fetch analysis data with spatial filters.'

    site = get_object_or_404(Site, slug= site_slug)

    # Get merged catalog model
    db_merged_table, model = get_merged_catalog('project', site_slug)

    # Apply spatial filter 
    filter_class = spatial_filter(model)
    filter_instance = filter_class(request.GET, queryset=db_merged_table)
    queryset = filter_instance.qs 

    # Create pandas DataFrame as input for data analysis
    df = pd.DataFrame.from_records(queryset.values())

    # Perform data analysis
    processed_data = analysis_engine(df)

    return JsonResponse(processed_data)


# Function for data download client
def download_catalog(request, site_slug, catalog_type):
    'Download catalog according to the site slug and catalog type.'
    db_table, model = get_hypocenter_catalog('project', site_slug, catalog_type)
    get_model = apps.get_model('project', model)

    # http response
    response = HttpResponse(
        content_type = "text/csv",
        headers={"Content-Disposition": 'attachment; filename="catalog_download.csv"'}
    )

    # write header
    writer = csv.writer(response)
    headers = [field.name for field in get_model._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in db_table:
        writer.writerow([getattr(data, field.name) for field in get_model._meta.fields])
    
    return response