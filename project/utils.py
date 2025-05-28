from django.db import models
import plotly.graph_objects as go
from plotly.io import to_html
import pandas as pd
from django.apps import apps

mapbox_access_token = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'

# detail database requirements
REQUIRED_HYPO_CATALOG_COLUMNS = [
    'source_id',
    'source_lat',
    'source_lon',
    'source_depth_m',
    'source_origin_dt',
    'n_phases',
    'magnitude'
]

REQUIRED_PICKING_CATALOG_COLUMNS = [
    'source_id',
    'station_code',
    'p_arrival_dt',
    's_arrival_dt',
]

REQUIRED_STATION_COLUMNS = [
    'station_code',
    'network_code',
    'station_lat',
    'station_lon',
    'station_elev_m'
]

# get hypocenter catalog
def get_hypocenter_catalog(app_label, slug, catalog_type):
    'Get hypocenter catalog from model.'
    for model in apps.get_app_config(app_label).get_models():
        if f"{slug}_{catalog_type}_catalog" in str(model._meta.db_table):
            all_objects = model.objects.all()
            model_name = model.__name__
            break
    return all_objects, model_name


# get full merge catalog including detail picking data and station
def get_full_catalog(app_label, slug, catalog_type):
    'Get full catalog by merging hypocenter, picking, and station.'
    def _to_frame(dict_object:dict ):
        df = pd.DataFrame(list(dict_object.values()))
        return df
    
    # define db structure
    db_structure = {
            'picking': f'{slug}_picking_catalog',
            'hypocenter': f'{slug}_{catalog_type}_catalog',   
            'station': f'{slug}_station'
            }
    
    # initialize db_table for query
    db_tables = {
        'picking': None,
        'hypocenter': None,
        'station': None
    }

    # get all the tables
    for model in apps.get_app_config(app_label).get_models():
        db_name = model._meta.db_table
        for key, table_name in db_structure.items():
            if db_name == table_name:
                db_tables[key] = _to_frame(model.objects.all())
                break

    # validate the completeness of table
    missing_tables = [key for key, df in db_tables.items() if df is None]
    if missing_tables:
        raise ValueError(f"Missing tables: {', '.join(missing_tables)}")
    
    # validate required columns
    required_columns = {
        'picking': REQUIRED_PICKING_CATALOG_COLUMNS,
        'hypocenter': REQUIRED_HYPO_CATALOG_COLUMNS,
        'station': REQUIRED_STATION_COLUMNS
    }
    for table_key, df in db_tables.items():
        missing_cols = [col for col in required_columns[table_key] if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns in {table_key} table: {', '.join(missing_cols)}")

    # merging databases
    result = (
        db_tables['hypocenter']
        .merge(db_tables['picking'], on='source_id', how='inner')
        .merge(db_tables['station'], on='station_code', how='inner')
        .reset_index()
    )

    return result


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

