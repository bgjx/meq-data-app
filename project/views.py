from django.shortcuts import render
from django.shortcuts import get_object_or_404
from frontpage.models import Site
import pandas as pd
from project.utils import (get_hypocenter_catalog, 
                           get_station,
                           get_merged_catalog)
from . filters import table_filter
from django.http import HttpResponse, JsonResponse
from django.apps import apps
import csv


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
        date_filter = filter_class(request.GET, queryset=db_table)
        # update context
        context[f'table_{catalog_type}'] = date_filter.qs
        context[f'date_filter_{catalog_type}'] = date_filter

    return render(request, 'project/data-explore.html', context)


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


def get_meq_data(request, site_slug = None):
    'Get meq hypocenter data, define the center of map, and normalized the magnitude.'
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


def meq_maps(request, site_slug = None):
    'Generate map frame for meq distributions map'
    site = get_object_or_404(Site, slug=site_slug)
    mapbox_access_token = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'
    context = {
        'site': site,
        'MAPBOX_TOKEN': mapbox_access_token,
    }
    return render(request, 'project/event-distributions.html', context=context)


def data_analysis(request, site_slug = None):
    'Generate views for data analysis page.'
    site = get_object_or_404(Site, slug=site_slug)

    # Get merged catalog model
    db_merged_table, model = get_merged_catalog('project', site_slug)

    # Apply filter
    context = {
                'site': site,
                'full_merged_catalog': db_merged_table}
    
    return render(request, 'project/data-analysis.html', context)