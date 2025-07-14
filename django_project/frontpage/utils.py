from django.apps import apps

def get_updates(app_label:str) -> str:
    table_name = 'project_updates'
    models = apps.get_app_config(app_label).get_models() 
    for model in models:
        if table_name in str(model._meta.db_table):
            return model.__name__
    return None