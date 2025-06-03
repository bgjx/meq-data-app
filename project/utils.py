from django.db import models
import plotly.graph_objects as go
from plotly.io import to_html
import pandas as pd
from django.apps import apps

mapbox_access_token = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'

# get hypocenter catalog
def get_hypocenter_catalog(app_label, slug, catalog_type):
    'Get hypocenter catalog from model.'
    for model in apps.get_app_config(app_label).get_models():
        if f"{slug}_{catalog_type}_catalog" in str(model._meta.db_table):
            all_objects = model.objects.all()
            model_name = model.__name__
            break
    return all_objects, model_name


# get merged catalog view for complete data analysis
def get_merged_catalog(app_label, slug):
    'Get full catalog by merging hypocenter, picking, and station.'
    # get all the tables
    for model in apps.get_app_config(app_label).get_models():
        if f"{slug}_catalog_merged_view" in str(model._meta.db_table):
            all_objects = model.objects.all()
            model_name = model.__name__ 
            break
    return all_objects, model_name


def get_station(app_label, slug):
    'Get station data from station model'
    for model in apps.get_app_config(app_label).get_models():
        if f"{slug}_station" in model._meta.db_table:
            all_objects = model.objects.all()
            break
    return all_objects


def plot_table(dataframe):
    'Plo table from dataframe'
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(dataframe.columns),
                fill_color='gray',
                align='center'),
    cells=dict(values=[dataframe[col] for col in dataframe.columns.to_list()],
               fill_color='lavender',
               align='left'))
                    ])
    return to_html(fig, full_html = False, include_plotlyjs='cdn')


def analysis_engine(df: pd.DataFrame):
    'Do data preprocessing and return the data to feed the plotly plots'  

    # Statistic in number
    total_events = len(df['source_id'].drop_duplicates())
    total_phases = len(df['p_arrival_dt']) + len(df['s_arrival_dt'])
    total_stations = len(df['station_code'].drop_duplicates())

    result  = {
        'total_events': total_events,
        'total_phases': total_phases,
        'total_stations': total_stations
    }

    return result

