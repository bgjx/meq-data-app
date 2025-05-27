from django.shortcuts import render
from django.shortcuts import get_object_or_404
from frontpage.models import Site
import project.models as mdl
import pandas as pd
import project.utils as utl
from . filters import dynamic_filter
from django.http import HttpResponse, JsonResponse
from django.apps import apps
import csv


def project_site(request, site_slug = None):
    site = get_object_or_404(Site, slug=site_slug)

    # find the specific models matching the site_slug and type of catalog
    db_table_relocated, model_relocated = utl.get_model(mdl, site_slug, "relocated")
    db_table_initial, model_initial = utl.get_model(mdl, site_slug, "initial")

    # apply filter on relocated catalog
    filter_relocated = dynamic_filter(model_relocated)
    date_filter_relocated = filter_relocated(request.GET, queryset=db_table_relocated)
    db_table_relocated = date_filter_relocated.qs

    # apply filter on relocated catalog
    filter_initial = dynamic_filter(model_initial)
    date_filter_initial = filter_initial(request.GET, queryset=db_table_initial)
    db_table_initial = date_filter_initial.qs

    context = {
        'site': site,
        'table_relocated': db_table_relocated,
        'date_filter_relocated':date_filter_relocated,
        'table_initial': db_table_initial,
        'date_filter_initial': date_filter_initial
    }

    return render(request, 'project/data-explore.html', context)


def download_csv_reloc(request, site_slug = None):
    db_table_relocated, model_relocated = utl.get_model(mdl, site_slug, "relocated")
    get_model_relocated = apps.get_model('project', model_relocated)

    response = HttpResponse(
        content_type = "text/csv",
        headers={"Content-Disposition": 'attachment; filename="catalog_relocated.csv"'}
    )

    writer = csv.writer(response)
    headers = [field.name for field in get_model_relocated._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in db_table_relocated:
        writer.writerow([getattr(data, field.name) for field in get_model_relocated._meta.fields])
    
    return response

def download_csv_initial(request, site_slug = None):
    db_table_initial, model_initial = utl.get_model(mdl, site_slug, "initial")
    get_model_initial = apps.get_model('project', model_initial)

    response = HttpResponse(
        content_type = "text/csv",
        headers={"Content-Disposition": 'attachment; filename="catalog_initial.csv"'}
    )

    writer = csv.writer(response)
    headers = [field.name for field in get_model_initial._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in db_table_initial:
        writer.writerow([getattr(data, field.name) for field in get_model_initial._meta.fields])
    return response


def get_meq_data(request, site_slug = None):
    # find the specific models matching the site_slug and type of catalog
    db_table_relocated, model_relocated = utl.get_model(mdl, site_slug, "relocated")
    db_table_initial, model_initial = utl.get_model(mdl, site_slug, "initial")
    db_station = utl.get_station(mdl, site_slug)

    # initialize dataframe for relocated earthquake
    df_meq_relocated = pd.DataFrame(list(db_table_relocated.values()))
    df_meq_relocated = df_meq_relocated[['source_id', 'source_lat', 'source_lon', 'source_depth_m', 'magnitude']]
   
    # do normalization data
    average_mw_relocated = df_meq_relocated.magnitude.mean()
    df_meq_relocated['magnitude'] = df_meq_relocated['magnitude'].fillna(average_mw_relocated) # fill empty magnitude column

    min_mag_relocated = df_meq_relocated.magnitude.min()
    normalize_mag_relocated = [1*((-1*min_mag_relocated)+data) for data in list(df_meq_relocated.magnitude)]
    df_meq_relocated['norm_magnitude'] = normalize_mag_relocated

    # Initialize dataframe for initial earthquake
    df_meq_initial = pd.DataFrame(list(db_table_initial.values()))
    df_meq_initial = df_meq_initial[['source_id', 'source_lat', 'source_lon', 'source_depth_m', 'magnitude']]

    # do normalization data
    average_mw_initial = df_meq_initial.magnitude.mean()
    df_meq_initial['magnitude'] = df_meq_initial['magnitude'].fillna(average_mw_initial) # fill empty magnitude column
    min_mag_initial = df_meq_initial.magnitude.min()
    normalize_mag_initial = [1*((-1*min_mag_initial)+data) for data in list(df_meq_initial.magnitude)]
    df_meq_initial['norm_magnitude'] = normalize_mag_initial

    # station dataframe
    df_station = pd.DataFrame(list(db_station.values()))

    # find center of the maps
    if site_slug == 'seml':
        center_map = dict(
            lat = -1.616487, 
            lon = 101.137171 
        )
    elif site_slug == 'serd':
        center_map = dict(
            lat = -4.220185, 
            lon = 103.379187 
        )
    else:
        pass

    data = {
        'meq_relocated': df_meq_relocated.to_dict(orient='records'),
        'meq_initial': df_meq_initial.to_dict(orient='records'),
        'station': df_station.to_dict(orient='records'),
        'center_map': center_map,
    }
    return JsonResponse(data)

def meq_maps(request, site_slug = None):
    site = get_object_or_404(Site, slug=site_slug)
    mapbox_access_token = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'
    context = {
        'site': site,
        'MAPBOX_TOKEN': mapbox_access_token,
    }
    return render(request, 'project/event-distributions.html', context=context)


def data_analysis(request, site_slug = None):
    site = get_object_or_404(Site, slug=site_slug)

    # find the specific models matching the site_slug and type of catalog
    db_table_relocated, model_relocated = utl.get_model(mdl, site_slug, "relocated")
    db_table_initial, model_initial = utl.get_model(mdl, site_slug, "initial")

    # get the DataFrame
    relocated_df = pd.DataFrame(list(db_table_relocated.values()))
    initial_df = pd.DataFrame(list(db_table_initial.values()))

    # get total earthquake and total phases
    
    context = {
        'site': site,
        'table_wcc': db_table_relocated,
        'table_nll': db_table_initial
    }
    
    return render(request, 'project/data-analysis.html', context)