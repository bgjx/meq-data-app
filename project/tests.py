from django.db import models
from django.test import TestCase
import project.models as mdl

# get the model 
# def get_model(model, slug, cat_type):
#     for model_name, model_value in model.__dict__.items():
#         if isinstance(model_value, type) and issubclass(model_value, models.Model):
#             if f"{slug}_cat_{cat_type}" in str(model_value._meta.db_table):
#                 all_objects = model_value.objects.all()
#     return all_objects, model_value.__name__

# object, model_name = get_model(mdl, 'seml', 'wcc')
# print(model_name)