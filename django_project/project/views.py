from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from django.conf import settings
from django.contrib import messages

from frontpage.models import Site
from project.models import HypoCatalogUplaod
from project.utils import (get_hypocenter_catalog, 
                           get_picking_catalog,
                           get_station,
                           get_merged_catalog,
                           analysis_engine)
from . filters import hypo_table_filter, picking_table_filter, spatial_filter
from . forms import UploadFormCatalogCSV
from . data_cleanser import (clean_hypo_df

                            )


from datetime import datetime, timedelta
import pandas as pd
import csv
from io import TextIOWrapper
from . import config
import openai 

# variable
MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN


# Open AI data descriptor 

# Function for page view renderer
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

    # update context
    context['station_table'] = get_model_station.objects.all()

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
    headers = [field.name for field in get_model._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in filter_instance.qs:
        writer.writerow([getattr(data, field.name) for field in get_model._meta.fields])
    
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
    headers = [field.name for field in get_model._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in filter_instance.qs:
        writer.writerow([getattr(data, field.name) for field in get_model._meta.fields])

    return response


def download_station(request, site_slug):
    'Download station data according to site slug'

    # Get model name
    model = get_station('project', site_slug)

    # Get reference model
    get_model = apps.get_model('project', model)

    # Http response
    response = HttpResponse(
        content_type = "text# View functions for data download client/csv; charset=utf-8",
         headers={"Content-Disposition": 'attachment; filename="station_download.csv"'}
    )

    # write header 
    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in get_model._meta.fields]
    writer.writerow(headers)

    # writing data
    for data in get_model.objects.all():
        writer.writerow([getattr(data, field.name) for field in get_model._meta.fields])
    
    return response# Get the model reference

# Data Uploading views
def read_hypo_file(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Could not read CSV file: {e}")
    
    # check missing columns
    missing_columns = set(config.REQUIRED_HYPO_COLUMNS_NAME) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {", ".join(missing_columns)}")
    
    return df


def save_dataframe_to_db(model, df:pd.DataFrame, overwrite=False):
    for _, row in df.iterrows():
        row_data = {k: (v if pd.notna(v) else None) for k,v in row.items()}
        sid = row.pop('source_id')
        if overwrite:
            model.objects.update_or_create(
                source_id = sid,
                defaults  = row_data
            )
        else:
            model.objects.get_or_create(
                source_id = sid,
                defaults = row_data
            )


def upload_form(request, site_slug):
    'Upload form for updating database'

    site = get_object_or_404(Site,slug=site_slug)

    if request.method == 'POST' and 'confirm_upload' in request.POST:
        # confirm and save
        overwrite = request.POST.get('overwrite') == True
        df_records = request.session.get('csv_data')

        if df_records:
            df = pd.DataFrame.from_records(df_records)
            save_dataframe_to_db(get_model, df, overwrite=overwrite)
            del request.session['csv_data']
            messages.success(request, 'CSV data uploaded successfully.')
        else:
            messages.error(request, 'No CSV data to upload.')
        
        return redirect('project:upload-hypo-catalog')

    elif request.method == 'POST':
        form = UploadFormCatalogCSV(request.POST, request.FILES)
        if form.is_valid():
            catalog_type = form.cleaned_data['catalog_type']
            uploaded_file = form.cleaned_data['file']

            if catalog_type == 'initial':
                # Get model reference
                model = get_hypocenter_catalog('project', site_slug, catalog_type)
                get_model = apps.get_model('project', model)

                try:
                    df = read_hypo_file(uploaded_file)
                    df = clean_hypo_df(df)

                    # find conflicting ids
                    conflicting_ids = list(
                        get_model.objects
                        .filter(source_id__in = df['source_id'].tolist())
                        .values_list('source_id', flat=True)
                    )

                    # preview data
                    preview_data = df.head().to_dict(orient='records')
                    request.session['csv_data'] = df.to_dict(orient='records')

                    context = {
                        'site': site,
                        'form': form,
                        'conflicts': conflicting_ids,
                        'preview': preview_data,
                        'overwrite': bool(conflicting_ids)
                    }

                    # update the upload models
                    HypoCatalogUplaod.objects.create(
                        title = form.cleaned_data['title'],
                        type = "initial catalog",
                        description = form.cleaned_data['description'],
                        file_name = form.cleaned_data['file'].name
                    )
                        
                    return render(request, 'project/uploads/upload-confirm.html', context)

                except Exception as e :
                    messages.error(request, f"Error processing {catalog_type} catalog CSV file: {e}")
                    return redirect('project:upload-form')
                
            elif catalog_type == 'relocated':
                # Get model reference
                model = get_hypocenter_catalog('project', site_slug, catalog_type)
                get_model = apps.get_model('project', model)

                try:
                    df = read_hypo_file(uploaded_file)
                    df = clean_hypo_df(df)

                    # find conflicting ids
                    conflicting_ids = list(
                        get_model.objects
                        .filter(source_id__in = df['source_id'].tolist())
                        .values_list('source_id', flat=True)
                    )

                    # preview data
                    preview_data = df.head().to_dict(orient='records')
                    request.session['csv_data'] = df.to_dict(orient='records')

                    context = {
                        'site': site,
                        'type': f"Hypocenter {catalog_type.capitalize()} Catalog",
                        'form': form,
                        'conflicts': conflicting_ids,
                        'preview': preview_data,
                        'overwrite': bool(conflicting_ids)
                    }

                    # update the upload models
                    HypoCatalogUplaod.objects.create(
                        title = form.cleaned_data['title'],
                        type = f" {catalog_type} catalog",
                        description = form.cleaned_data['description'],
                        file_name = form.cleaned_data['file'].name
                    )
                        
                    return render(request, 'project/uploads/upload-confirm.html', context)

                except Exception as e :
                    messages.error(request, f"Error processing {catalog_type} catalog CSV file: {e}")
                    return redirect('project:upload-form')
            else:
                return redirect('project:upload-form')
        
    else:
        form = UploadFormCatalogCSV()
    
    context ={
        'site': site,
        'form': form,
    }
    
    return render(request, 'project/upload-form.html', context)


# def meq_maps(request, site_slug = None):
#     'Generate map frame for meq distributions map'
#     site = get_object_or_404(Site, slug=site_slug)
#     mapbox_access_token = MAPBOX_API_TOKEN
#     context = {
#         'site': site,
#         'MAPBOX_TOKEN': mapbox_access_token,
#     }
#     return render(request, 'project/event-distributions.html', context=context)# Function for data download client


# #  API endpoint function
# def get_meq_data(request, site_slug = None):
#     'API endpoint to get hypocenter data and calculate the center point'

#     site = get_object_or_404(Site, slug=site_slug)    
#     # map center
#     center_map = {
#         'seml': {'lat': -1.616487, 'lon':101.137171},
#         'serd': {'lat': -4.220185, 'lon': 103.379187}
#     }

#     # define catalog type
#     catalog_types = [
#         {'type': 'relocated'},
#         {'type': 'initial'}
#     ]
    
#     # get station dataframe
#     db_station = get_station('project', site_slug)
#     df_station = pd.DataFrame(list(db_station.values()))

#     data = {
#         'station': df_station.to_dict(orient='records'),
#         'center_map': center_map[site_slug]
#     }

#     # get hypocenter dataframe and normalize magnitude 
#     for catalog in catalog_types:
#         catalog_type = catalog['type']
#         db_table, model = get_hypocenter_catalog('project', site_slug, catalog_type)
#         df_meq = pd.DataFrame(list(db_table.values()))
#         df_meq = df_meq[['source_id', 'source_lat', 'source_lon', 'source_depth_m', 'magnitude']]
        
#         # magnitude normalization
#         average_magnitude = df_meq.magnitude.median()
#         df_meq['magnitude'] = df_meq['magnitude'].fillna(average_magnitude)

#         min_magnitude = df_meq.magnitude.min()
#         normalized_magnitude = [1 * (( -1 * min_magnitude) + data) for data in list(df_meq.magnitude)]
#         df_meq['norm_magnitude'] = normalized_magnitude

#         # update data object
#         data[f'meq_{catalog_type}'] = df_meq.to_dict(orient='records')

#     return JsonResponse(data)


def data_analysis(request, site_slug = None):
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


def get_analysis_data( request, site_slug=None):
    'API endpoint to fetch analysis data with spatial filters.'

    site = get_object_or_404(Site, slug= site_slug)

    # Get merged catalog model name
    model = get_merged_catalog('project', site_slug)

    # Get reference model
    get_model = apps.get_model('project', model)

    # Apply spatial filter 
    filter_class = spatial_filter(model)
    filter_instance = filter_class(request.GET, queryset=get_model.objects.all())
    queryset = filter_instance.qs 

    # Create pandas DataFrame as input for data analysis
    df = pd.DataFrame.from_records(queryset.values())

    # Perform data analysis
    processed_data = analysis_engine(df, site_slug)

    return JsonResponse(processed_data)

