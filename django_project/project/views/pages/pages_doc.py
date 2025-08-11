from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from frontpage.models import Site
from project.models import Updates
from project.utils import (get_hypocenter_catalog, 
                           get_picking_catalog,
                           get_station)

from project.filters import hypo_table_filter, picking_table_filter
from project.forms import UploadFormCatalogCSV
from project.data_cleanser import (clean_hypo_df,
                             clean_picking_df,
                             clean_station_df
                            )

from datetime import datetime, timedelta
import pandas as pd
import csv
from project.config import DATA_STRUCTURES, REQUIREMENTS

MAPBOX_API_TOKEN = settings.MAPBOX_API_TOKEN


@login_required
def project_site(request, site_slug: str = None) -> HttpResponse:
    """View function for the data explorer page.

    Args:
        request (HttpRequest): The HTTP request object.
        site_slug (str, optional): The slug of the site. Defaults to None.

    Returns:
        HttpResponse: The rendered response with the context.
    """
    
    site = get_object_or_404(Site, slug=site_slug)

    catalog_types = [
        {'type': 'relocated', 'download_url': 'download-relocated'},
        {'type': 'initial', 'download_url': 'download-initial'}
    ]

    context = {'site': site}
    
    # hypocenter data
    for catalog in catalog_types:
        catalog_type = catalog['type']
        model_hypo = get_hypocenter_catalog('project', site_slug, catalog_type)
        hypo_filter_class = hypo_table_filter(model_hypo)
        hypo_filter_instance = hypo_filter_class(request.GET, queryset=model_hypo.objects.all())
        context[f'hypo_table_{catalog_type}'] = hypo_filter_instance.qs
        context[f'hypo_date_filter_{catalog_type}'] = hypo_filter_instance
    
    # picking data
    model_picking = get_picking_catalog('project', site_slug)
    picking_filter_class = picking_table_filter(model_picking)
    picking_filter_instance = picking_filter_class(request.GET, queryset=model_picking.objects.all())
    context['picking_table'] = picking_filter_instance.qs
    context['picking_date_filter'] = picking_filter_instance

    # station data
    model_station = get_station('project', site_slug)

    # check role user (Admins or Guest)
    is_admin = request.user.groups.filter(name='Admins').exists()

    # update context
    context['station_table'] = model_station.objects.all()
    context['is_admin'] = is_admin

    return render(request, 'project/data-explore.html', context)


def download_hypo_catalog(request, site_slug: str, catalog_type: str) -> HttpResponse:
    """Download hypocenter catalog according to the site slug and catalog type.

    Args:
        request (HttpRequest): The HTTP request object.
        site_slug (str): The slug of the site.
        catalog_type (str): The type of the catalog.

    Returns:
        HttpResponse: The CSV file response containing hypocenter data.
    """
    
    model_hypo = get_hypocenter_catalog('project', site_slug, catalog_type)
    filter_class = hypo_table_filter(model_hypo)
    filter_instance = filter_class(request.GET, queryset=model_hypo.objects.all())

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="hypo_catalog_download.csv"'}
    )

    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in model_hypo._meta.fields[:-1]]
    writer.writerow(headers)

    for data in filter_instance.qs:
        writer.writerow([getattr(data, header) for header in headers])
    
    return response


def download_picking_catalog(request, site_slug: str) -> HttpResponse:
    """Download picking catalog according to the site slug.

    Args:
        request (HttpRequest): The HTTP request object.
        site_slug (str): The slug of the site.

    Returns:
        HttpResponse: The CSV file response containing picking data.
    """
    
    model_picking = get_picking_catalog('project', site_slug)
    filter_class = picking_table_filter(model_picking)
    filter_instance = filter_class(request.GET, queryset=model_picking.objects.all())

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="picking_catalog_download.csv"'}
    )

    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in model_picking._meta.fields[1:]]
    writer.writerow(headers)

    for data in filter_instance.qs:
        writer.writerow([getattr(data, header) for header in headers])

    return response


def download_station(request, site_slug: str) -> HttpResponse:
    """Download station data according to the site slug.

    Args:
        request (HttpRequest): The HTTP request object.
        site_slug (str): The slug of the site.

    Returns:
        HttpResponse: The CSV file response containing station data.
    """
    
    model_station = get_station('project', site_slug)

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="station_download.csv"'}
    )

    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in model_station._meta.fields[1:]]
    writer.writerow(headers)

    for data in model_station.objects.all():
        writer.writerow([getattr(data, header) for header in headers])
    
    return response


def read_csv_file(csv_file, data_type: str) -> pd.DataFrame:
    """Read a CSV file and validate its contents against required columns.

    Args:
        csv_file (str): The path to the CSV file.
        data_type (str): The type of data being uploaded.

    Raises:
        ValueError: If CSV could not be read or required columns are missing.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    
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


def save_dataframe_to_db(app_name: str, model_name: str, lookup_fields: list[str], df: pd.DataFrame, overwrite: bool = False) -> None:
    """Save the DataFrame to the database, updating or creating records as needed.

    Args:
        app_name (str): The name of the Django app.
        model_name (str): The name of the Django model.
        lookup_fields (list[str]): Fields used for looking up existing records.
        df (pd.DataFrame): The DataFrame with records to save.
        overwrite (bool, optional): Whether to overwrite existing records. Defaults to False.
    """
    
    model = apps.get_model(app_name, model_name)
    for _, row in df.iterrows():
        row_data = {k: (v if pd.notna(v) else None) for k, v in row.items()}
        lookup_data = {field: row_data.pop(field) for field in lookup_fields}
        if overwrite:
            model.objects.update_or_create(
                **lookup_data,
                defaults=row_data
            )
        else:
            model.objects.get_or_create(
                **lookup_data,
                defaults=row_data
            )


def upload_form(request, site_slug: str) -> HttpResponse:
    """Upload form for updating the database.

    Args:
        request (HttpRequest): The HTTP request object.
        site_slug (str): The slug of the site.

    Returns:
        HttpResponse: The rendered response with the upload form.
    """
    
    site = get_object_or_404(Site, slug=site_slug)

    data_structure_tabs = [
        {'label': 'Hypo Catalog', 'data_tab': 'tab-hypo', 'active': True},
        {'label': 'Picking Catalog', 'data_tab': 'tab-picking', 'active': False},
        {'label': 'Station Catalog', 'data_tab': 'tab-station', 'active': False},
    ]

    if request.method == 'POST' and 'confirm_upload' in request.POST:
        # confirm and save
        overwrite = request.POST.get('overwrite') == "true"
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
                model_hypo = get_hypocenter_catalog('project', site_slug, data_type)
                try:
                    df = read_csv_file(uploaded_file, 'hypo')
                    df = clean_hypo_df(df)

                    conflicting_ids = list(
                        model_hypo.objects
                        .filter(source_id__in=df['source_id'].tolist())
                        .values_list('source_id', flat=True)
                    )

                    Updates.objects.create(
                        site_project=site_slug,
                        username=request.user.username,
                        title=form.cleaned_data['title'],
                        type=f'{data_type} catalog',
                        description=form.cleaned_data['description'],
                        file_name=form.cleaned_data['file'].name
                    )

                    preview_data = df.head().to_dict(orient='records')
                    request.session['app_name'] = 'project'
                    request.session['model_name'] = model_hypo._meta.model_name
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

                except Exception as e:
                    messages.error(request, f"Error processing {data_type} catalog file: {e}")
                    return redirect('project:upload-form')
                
            elif data_type == 'picking':
                model_picking = get_picking_catalog('project', site_slug) 
                
                try:
                    df = read_csv_file(uploaded_file, 'picking')
                    df = clean_picking_df(df)

                    conflicting_ids = list(
                        model_picking.objects
                        .filter(source_id__in=df['source_id'].unique().tolist())
                        .values_list('source_id', flat=True)
                        .distinct()
                    )

                    Updates.objects.create(
                        site_project=site_slug,
                        username=request.user.username,
                        title=form.cleaned_data['title'],
                        type="picking catalog",
                        description=form.cleaned_data['description'],
                        file_name=form.cleaned_data['file'].name
                    )

                    preview_data = df.head().to_dict(orient='records')
                    request.session['app_name'] = 'project'
                    request.session['model_name'] = model_picking._meta.model_name
                    request.session['csv_data'] = df.to_dict(orient='records')
                    request.session['lookup_fields'] = ['source_id', 'station_code']

                    context = {
                        'site': site,
                        'form': form,
                        'conflicts': conflicting_ids,
                        'preview': preview_data,
                        'overwrite': bool(conflicting_ids)
                    }
                    return render(request, 'project/uploads/upload-confirm.html', context)
                
                except Exception as e:
                    messages.error(request, f"Error processing {data_type} catalog CSV file: {e}")
                    return redirect('project:upload-form')
            
            elif data_type == 'station':
                model_station = get_station('project', site_slug)

                try:
                    df = read_csv_file(uploaded_file, 'station')
                    df = clean_station_df(df)

                    conflicting_stations = list(
                        model_station.objects
                        .filter(station_code__in=df['station_code'].tolist())
                        .values_list('station_code', flat=True)
                    )

                    Updates.objects.create(
                        site_project=site_slug,
                        username=request.user.username,
                        title=form.cleaned_data['title'],
                        type="station data",
                        description=form.cleaned_data['description'],
                        file_name=form.cleaned_data['file'].name
                    )

                    preview_data = df.head().to_dict(orient='records')
                    request.session['app_name'] = 'project'
                    request.session['model_name'] = model_station._meta.model_name
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
    
    context = {
        'site': site,
        'form': form,
        'tabs': data_structure_tabs,
        'data_structure': DATA_STRUCTURES
    }
    
    return render(request, 'project/upload-form.html', context)


def general_performance(request, site_slug: str = None) -> HttpResponse:
    """Generate views for general analysis page.

    Args:
        request (HttpRequest): The HTTP request object.
        site_slug (str, optional): The slug of the site. Defaults to None.

    Returns:
        HttpResponse: The rendered response with the general performance context.
    """
    
    site = get_object_or_404(Site, slug=site_slug)

    # get current datetime
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    w_before = now - timedelta(days=7)
    w_before_str = w_before.strftime("%Y-%m-%d %H:%M:%S") 

    mapbox_access_token = MAPBOX_API_TOKEN

    context = {
        'site': site,
        'now_time': now_str,
        'week_before_time': w_before_str,
        'MAPBOX_TOKEN': mapbox_access_token,
    }
    
    return render(request, 'project/general-performance.html', context)


def detail_analytics(request, site_slug: str = None) -> HttpResponse:
    """Generate views for detail analytics page.

    Args:
        request (HttpRequest): The HTTP request object.
        site_slug (str, optional): The slug of the site. Defaults to None.

    Returns:
        HttpResponse: The rendered response with the detail analytics context.
    """
    
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
    
    return render(request, 'project/detail-analytics.html', context)
