import project.models as mdl
from django.db import models
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.io import to_html
import pandas as pd
from datetime import datetime

mapbox_access_token = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'
# get the model 
def get_model(model, slug, cat_type):
    for model_name, model_value in model.__dict__.items():
        if isinstance(model_value, type) and issubclass(model_value, models.Model):
            if f"{slug}_cat_{cat_type}" in str(model_value._meta.db_table):
                all_objects = model_value.objects.all()
                model_name = model_value.__name__
                break
    return all_objects, model_name

def get_station(model, slug):
    for model_name, model_value in model.__dict__.items():
        if isinstance(model_value, type) and issubclass(model_value, models.Model):
            if f"{slug}_station" in str(model_value._meta.db_table):
                all_objects = model_value.objects.all()
                break
    return all_objects

# plotting table
def plot_table(dataframe):
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(dataframe.columns),
                fill_color='gray',
                align='center'),
    cells=dict(values=[dataframe[col] for col in dataframe.columns.to_list()],
               fill_color='lavender',
               align='left'))
                    ])
    return to_html(fig, full_html = False, include_plotlyjs='cdn')

