from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from frontpage.models import Site
from project.models import Updates
from project.utils import (get_hypocenter_catalog, 
                           get_picking_catalog,
                           get_station,
                           get_merged_catalog,
                           analysis_engine)

from . filters import hypo_table_filter, picking_table_filter, spatial_filter
from . forms import UploadFormCatalogCSV
from . data_cleanser import (clean_hypo_df,
                             clean_picking_df,
                             clean_station_df
                            )

from analytics.base import validate_dataframe, preprocess_dataframe
from analytics.general import (
    compute_general_statistics,
    compute_overall_daily_intensities,
    compute_station_performance,
    compute_time_series_performance,
    retrieve_catalog_hypocenter
)
from analytics.wadati import compute_wadati_profile
from analytics.gutenberg import gutenberg_analysis

from datetime import datetime, timedelta
import pandas as pd
import csv
from io import TextIOWrapper
from . config import DATA_STRUCTURES, REQUIREMENTS
import openai 

# variable
MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN


# Open AI data descriptor 

# Function for page view renderer
@login_required
def project_site(request, site_slug = None):
    'View function for data explorer page.'
    site = get_object_or_404(Site, slug=site_slug)

    # Define catalog types and their download URLs
    catalog_types = [
        {'type': 'relocated', 'download_url':'download-relocated'},
        {'type': 'initial', 'download_url': 'download-initial'}
    ]

    #  Process table
    context = {'site': site}

    # For hypocenter catalog
    for catalog in catalog_types:
        catalog_type = catalog['type']

        # Get model
        hypo_model_name = get_hypocenter_catalog('project', site_slug, catalog_type)
        get_model_hypo = apps.get_model('project', hypo_model_name)

        # apply filter
        hypo_filter_class = hypo_table_filter(hypo_model_name)
        hypo_filter_instance = hypo_filter_class(request.GET, queryset=get_model_hypo.objects.all())

        # update context
        context[f'hypo_table_{catalog_type}'] = hypo_filter_instance.qs
        context[f'hypo_date_filter_{catalog_type}'] = hypo_filter_instance
    
    # For picking catalog
    # Get model
    picking_model_name = get_picking_catalog('project', site_slug)
    get_model_picking = apps.get_model('project', picking_model_name)
    
    # Apply filter 
    picking_filter_class = picking_table_filter(picking_model_name)
    picking_filter_instance = picking_filter_class(request.GET, queryset=get_model_picking.objects.all())

    # update context
    context['picking_table'] = picking_filter_instance.qs
    context['picking_date_filter'] = picking_filter_instance

    # For station
    # Get model
    station_model_name = get_station('project', site_slug)
    get_model_station = apps.get_model('project', station_model_name)

    # check role user (Admins or Guest)
    is_admin = request.user.groups.filter(name='Admins').exists()

    # update context
    context['station_table'] = get_model_station.objects.all()
    context['is_admin'] = is_admin

    return render(request, 'project/data-explore.html', context)


# View functions for data download client
def download_hypo_catalog(request, site_slug, catalog_type):
    'Download hypocenter catalog according to the site slug and catalog type.'

    # Get model name
    model = get_hypocenter_catalog('project', site_slug, catalog_type)
    
    # Get reference model
    get_model = apps.get_model('project', model)

    # Applied filter with the model and request.GET parameters
    filter_class = hypo_table_filter(model)
    filter_instance = filter_class(request.GET, queryset=get_model.objects.all())

    # http response
    response = HttpResponse(
        content_type = "text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="hypo_catalog_download.csv"'}
    )

    # write header
    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in get_model._meta.fields[:-1]]
    writer.writerow(headers)

    # writing data
    for data in filter_instance.qs:
        writer.writerow([getattr(data, header) for header in headers])
    
    return response


def download_picking_catalog(request, site_slug):
    'Download picking catalog according to the site slug'

    # Get model name
    model = get_picking_catalog('project', site_slug)

    # Get reference model 
    get_model = apps.get_model('project', model)

    # Applied filter with the model and request.GET parameters
    filter_class = picking_table_filter(model)
    filter_instance = filter_class(request.GET, queryset=get_model.objects.all())

    # Http response
    response = HttpResponse(
        content_type = "text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="picking_catalog_download.csv"'}
    )

    # write header
    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in get_model._meta.fields[1:]]
    writer.writerow(headers)

    # writing data
    for data in filter_instance.qs:
        writer.writerow([getattr(data, header) for header in headers])

    return response


def download_station(request, site_slug):
    'Download station data according to site slug'

    # Get model name
    model = get_station('project', site_slug)

    # Get reference model
    get_model = apps.get_model('project', model)

    # Http response
    response = HttpResponse(
        content_type = "text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="station_download.csv"'}
    )

    # write header 
    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in get_model._meta.fields[1:]]
    writer.writerow(headers)

    # writing data
    for data in get_model.objects.all():
        writer.writerow([getattr(data, header) for header in headers])
    
    return response


# CSV file read method
def read_csv_file(csv_file, data_type):
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Could not read CSV file: {e}")

    # Check missing columns
    columns_check = REQUIREMENTS[data_type]
    missing_columns = [col for col in columns_check if col not in df.columns]
    if missing_columns:
        raise ValueError(f'Missing columns: {", ".join(missing_columns)}')

    return df

# Save to database method
def save_dataframe_to_db(app_name:str, model_name:str, lookup_fields:list[str], df:pd.DataFrame, overwrite=False):

    # get the model reference
    model = apps.get_model(app_name, model_name)
    for _, row in df.iterrows():
        row_data = {k: (v if pd.notna(v) else None) for k,v in row.items()}
        lookup_data = {field: row_data.pop(field) for field in lookup_fields}
        if overwrite:
            model.objects.update_or_create(
                **lookup_data,
                defaults  = row_data
            )
        else:
            model.objects.get_or_create(
                **lookup_data,
                defaults = row_data
            )


def upload_form(request, site_slug):
    'Upload form for updating database'

    # Get the site models reference
    site = get_object_or_404(Site, slug=site_slug)

    ## data structure views
    # data structure tabs
    data_structure_tabs = [
        {'label': 'Hypo Catalog', 'data_tab': 'tab-hypo', 'active': True},
        {'label': 'Picking Catalog', 'data_tab': 'tab-picking', 'active': False},
        {'label': 'Station Catalog', 'data_tab': 'tab-station', 'active': False},
    ]

    if request.method == 'POST' and 'confirm_upload' in request.POST:
        # confirm and save
        overwrite = request.POST.get('overwrite') == True
        app_name = request.session.get('app_name')
        model_name = request.session.get('model_name')
        lookup_fields = request.session.get('lookup_fields')
        df_records = request.session.get('csv_data')

        if df_records:
            df = pd.DataFrame.from_records(df_records)
            save_dataframe_to_db(app_name, model_name, lookup_fields, df, overwrite=overwrite)
            del request.session['csv_data']
            messages.success(request, 'CSV data uploaded successfully.')
        else:
            messages.error(request, 'No CSV data to upload.')
        
        return redirect('project:upload-form', site_slug=site_slug)

    elif request.method == 'POST':
        form = UploadFormCatalogCSV(request.POST, request.FILES)
        if form.is_valid():
            data_type = form.cleaned_data['data_type']
            uploaded_file = form.cleaned_data['file']

            if data_type in ['initial', 'relocated']:
                # Get model reference
                model = get_hypocenter_catalog('project', site_slug, data_type)
                get_model = apps.get_model('project', model)

                try:
                    df = read_csv_file(uploaded_file, 'hypo')
                    df = clean_hypo_df(df)

                    # find conflicting ids
                    conflicting_ids = list(
                        get_model.objects
                        .filter(source_id__in = df['source_id'].tolist())
                        .values_list('source_id', flat=True)
                    )

                    # update the upload models
                    Updates.objects.create(
                        site_project = site_slug,
                        username = request.user.username,
                        title = form.cleaned_data['title'],
                        type = f'{data_type} catalog',
                        description = form.cleaned_data['description'],
                        file_name = form.cleaned_data['file'].name
                    )

                    # preview data (look_up is given **kwargs parameters for model update_or_create)
                    preview_data = df.head().to_dict(orient='records')
                    request.session['app_name'] = 'project'
                    request.session['model_name'] = model
                    request.session['csv_data'] = df.to_dict(orient='records')
                    request.session['lookup_fields'] = ['source_id']

                    context = {
                        'site': site,
                        'form': form,
                        'conflicts': conflicting_ids,
                        'preview': preview_data,
                        'overwrite': bool(conflicting_ids)
                    }    

                    return render(request, 'project/uploads/upload-confirm.html', context)

                except Exception as e :
                    messages.error(request, f"Error processing {data_type} catalog file: {e}")
                    return redirect('project:upload-form')
                
            elif data_type == 'picking':
                # Get model reference
                model = get_picking_catalog('project', site_slug) 
                get_model = apps.get_model('project', model)
                
                try:
                    df = read_csv_file(uploaded_file, 'picking')
                    df = clean_picking_df(df)

                    # find conflicting ids
                    conflicting_ids = list(
                        get_model.objects
                        .filter(source_id__in = df['source_id'].unique().tolist())
                        .values_list('source_id', flat=True)
                        .distinct()
                    )

                    # update the upload models
                    Updates.objects.create(
                        site_project = site_slug,
                        username = request.user.username,
                        title = form.cleaned_data['title'],
                        type = "picking catalog",
                        description = form.cleaned_data['description'],
                        file_name = form.cleaned_data['file'].name
                    )

                    # preview data (look_up is given **kwargs parameters for model update_or_create)
                    preview_data = df.head().to_dict(orient='records')
                    request.session['app_name'] = 'project'
                    request.session['model_name'] = model
                    request.session['csv_data'] = df.to_dict(orient='records')
                    request.session['lookup_fields'] = ['source_id', 'station_code']

                    context = {
                        'site': site,
                        'form': form,
                        'conflicts': conflicting_ids,
                        'preview': preview_data,
                        'overwrite': bool(conflicting_ids)
                    }
                    return render (request, 'project/uploads/upload-confirm.html', context)
                
                except Exception as e:
                    messages.error(request, f"Error processing {data_type} catalog CSV file: {e}")
                    return redirect('project:upload-form')
            
            elif data_type == 'station':
                # Get model reference
                model = get_station('project', site_slug) 
                get_model = apps.get_model('project', model)

                try:
                    df = read_csv_file(uploaded_file, 'station')
                    df = clean_station_df(df)

                    # find conflicting station code
                    conflicting_stations = list(
                        get_model.objects
                        .filter(station_code__in = df['station_code'].tolist())
                        .values_list('station_code', flat=True)
                    )

                    # update the upload models
                    Updates.objects.create(
                        site_project = site_slug,
                        username = request.user.username,
                        title = form.cleaned_data['title'],
                        type = "station data",
                        description = form.cleaned_data['description'],
                        file_name = form.cleaned_data['file'].name
                    )

                    # preview data (look_up is given **kwargs parameters for model update_or_create)
                    preview_data = df.head().to_dict(orient='records')
                    request.session['app_name'] = 'project'
                    request.session['model_name'] = model
                    request.session['csv_data'] = df.to_dict(orient='records')
                    request.session['lookup_fields'] = ['station_code']

                    context = {
                        'site': site,
                        'form': form,
                        'conflicts': conflicting_stations,
                        'preview': preview_data,
                        'overwrite': bool(conflicting_stations)
                    }

                    return render(request, 'project/uploads/upload-confirm.html', context)
                
                except Exception as e:
                    messages.error(request, f'Error processing {data_type} csv file: {e}')
                    return redirect('project:upload-form')
                 
            else:
                return redirect('project:upload-form')
        
    else:
        form = UploadFormCatalogCSV()
    
    context ={
        'site': site,
        'form': form,
        'tabs': data_structure_tabs,
        'data_structure': DATA_STRUCTURES
    }
    
    return render(request, 'project/upload-form.html', context)


def general_performance(request, site_slug = None):
    'Generate views for data analysis page.'
    site = get_object_or_404(Site, slug=site_slug)

    # get current datetime
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    w_before = now - timedelta(days=7)
    w_before_str = w_before.strftime("%Y-%m-%d %H:%M:%S") 

    mapbox_access_token = MAPBOX_API_TOKEN

    context = {
                ''
                'site': site,
                'now_time': now_str,
                'week_before_time': w_before_str,
                'MAPBOX_TOKEN': mapbox_access_token,
    }
    
    return render(request, 'project/data-analysis.html', context)


# DRF Implementation for analysis data end point
class GeneralPerformanceAPIView(APIView):
    """
    API endpoints to fetch general performance of microearthquake monitoring.
    """
    def get(self, request, site_slug=None):

        site = get_object_or_404(Site, slug= site_slug)

        model = get_merged_catalog('project', site_slug)
        get_model = apps.get_model('project', model)

        filter_class = spatial_filter(model)
        filter_instance = filter_class(request.GET, queryset=get_model.objects.all())
        queryset = filter_instance.qs 

        df = pd.DataFrame.from_records(queryset.values())

        validated_df = validate_dataframe(df)

        if validated_df:
            hypocenter_df, picking_df = preprocess_dataframe(validated_df)

            data = {
                'general_statistic': compute_general_statistics(hypocenter_df, picking_df),
                'overall_daily_intensities': compute_overall_daily_intensities(picking_df),
                'hypocenter': retrieve_catalog_hypocenter(hypocenter_df, picking_df, site_slug)
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_204_NO_CONTENT)

