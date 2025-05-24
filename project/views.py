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

    # Get catalog type by request GET method
    catalog_type = request.GET.get('catalog_type', 'wcc')


    # find the specific models matching the site_slug and type of catalog
    db_table_wcc, model_wcc = utl.get_model(mdl, site_slug, "wcc")
    db_table_nll, model_nll = utl.get_model(mdl, site_slug, "nll")

    # apply filter wcc
    filter_wcc = dynamic_filter(model_wcc)
    date_filter_wcc = filter_wcc(request.GET, queryset=db_table_wcc)
    db_table_wcc = date_filter_wcc.qs

    # apply filter nll
    filter_nll = dynamic_filter(model_nll)
    date_filter_nll = filter_nll(request.GET, queryset=db_table_nll)
    db_table_nll = date_filter_nll.qs

    context = {
        'site': site,
        'table_wcc': db_table_wcc,
        'date_filter_wcc':date_filter_wcc,
        'table_nll': db_table_nll,
        'date_filter_nll': date_filter_nll
    }
    return render(request, 'project/data-explore.html', context)


def download_csv_wcc(request, site_slug = None):
    db_table_wcc, model_wcc = utl.get_model(mdl, site_slug, "wcc")
    get_model_wcc = apps.get_model('project', model_wcc)

    response = HttpResponse(
        content_type = "text/csv",
        headers={"Content-Disposition": 'attachment; filename="catalog_wcc.csv"'}
    )

    writer = csv.writer(response)
    headers = [field.name for field in get_model_wcc._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in db_table_wcc:
        writer.writerow([getattr(data, field.name) for field in get_model_wcc._meta.fields])
    
    return response

def download_csv_nll(request, site_slug = None):
    db_table_nll, model_nll = utl.get_model(mdl, site_slug, "nll")
    get_model_nll = apps.get_model('project', model_nll)

    response = HttpResponse(
        content_type = "text/csv",
        headers={"Content-Disposition": 'attachment; filename="catalog_nll.csv"'}
    )

    writer = csv.writer(response)
    headers = [field.name for field in get_model_nll._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in db_table_nll:
        writer.writerow([getattr(data, field.name) for field in get_model_nll._meta.fields])
    return response


def get_meq_data(request, site_slug = None):
    # find the specific models matching the site_slug and type of catalog
    db_table_wcc, model_wcc = utl.get_model(mdl, site_slug, "wcc")
    db_table_nll, model_nll = utl.get_model(mdl, site_slug, "nll")
    db_station = utl.get_station(mdl, site_slug)

    # initialize dataframe wcc
    df_meq_wcc = pd.DataFrame(list(db_table_wcc.values()))
    df_meq_wcc = df_meq_wcc[['event_id', 'lat', 'lon', 'depth_m', 'elev_m', 'mw_mag']]
   
    # do normalization data
    average_mw_wcc = df_meq_wcc.mw_mag.mean()
    df_meq_wcc['mw_mag'] = df_meq_wcc['mw_mag'].fillna(average_mw_wcc) # fill empty magnitude column

    min_mag_wcc = df_meq_wcc.mw_mag.min()
    normalize_mag_wcc = [1*((-1*min_mag_wcc)+data) for data in list(df_meq_wcc.mw_mag)]
    df_meq_wcc['norm_mw'] = normalize_mag_wcc

    # Initialize dataframe nll
    df_meq_nll = pd.DataFrame(list(db_table_nll.values()))
    df_meq_nll = df_meq_nll[['event_id', 'lat', 'lon', 'depth_m', 'elev_m', 'mw_mag']]

    # do normalization data
    average_mw_nll = df_meq_nll.mw_mag.mean()
    df_meq_nll['mw_mag'] = df_meq_nll['mw_mag'].fillna(average_mw_nll) # fill empty magnitude column
    min_mag_nll = df_meq_nll.mw_mag.min()
    normalize_mag_nll = [1*((-1*min_mag_nll)+data) for data in list(df_meq_wcc.mw_mag)]
    df_meq_nll['norm_mw'] = normalize_mag_nll

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
        'meq_wcc': df_meq_wcc.to_dict(orient='records'),
        'meq_nll': df_meq_nll.to_dict(orient='records'),
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
