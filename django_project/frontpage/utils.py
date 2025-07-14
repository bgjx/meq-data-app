from django.apps import apps

def get_updates(app_label:str) -> str:
    """
    Retrieve the name of the model corresponding to a specific database table.

    Args:
        app_label (str): The name of the Django app.

    Returns:
        str: The name of the model if it corresponds to the 'project_updates' 
             table, or None if not found.
    """
    table_name = 'project_updates'
    models = apps.get_app_config(app_label).get_models() 
    for model in models:
        if table_name in str(model._meta.db_table):
            return model.__name__
    return None