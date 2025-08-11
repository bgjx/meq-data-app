from django.apps import apps
from project.filters import spatial_filter

def get_hypocenter_catalog(app_label: str, slug: str, catalog_type: str) -> str:
    """
    Retrieve the hypocenter catalog model name for the specified app and catalog type.

    Args:
        app_label (str): The name of the Django app.
        slug (str): Slug used in the catalog name.
        catalog_type (str): The type of catalog to retrieve.

    Returns:
        str: The name of the model corresponding to the hypocenter catalog, or None if not found.
    """
    table_name = f"{slug}_{catalog_type}_catalog"
    models = apps.get_app_config(app_label).get_models()
    for model in models:
        if table_name in str(model._meta.db_table):
            return model.__name__
    return None


def get_picking_catalog(app_label: str, slug: str) -> str:
    """
    Retrieve the picking catalog model name for the specified app.

    Args:
        app_label (str): The name of the Django app.
        slug (str): Slug used in the catalog name.

    Returns:
        str: The name of the model corresponding to the picking catalog, or None if not found.
    """
    table_name = f"{slug}_picking_catalog"
    models = apps.get_app_config(app_label).get_models()
    for model in models:
        if table_name in str(model._meta.db_table):
            return model.__name__
    return None


def get_merged_catalog(app_label: str, slug: str) -> str:
    """
    Retrieve the merged catalog view model name for complete data analysis.

    Args:
        app_label (str): The name of the Django app.
        slug (str): Slug used in the catalog name.

    Returns:
        str: The name of the model corresponding to the merged catalog view, or None if not found.
    """
    table_name = f"{slug}_catalog_merged_view"
    models = apps.get_app_config(app_label).get_models()
    for model in models:
        if table_name in str(model._meta.db_table):
            return model
    return None


def get_station(app_label: str, slug: str) -> str:
    """
    Retrieve the station data model name from the specified app.

    Args:
        app_label (str): The name of the Django app.
        slug (str): Slug used in the station name.

    Returns:
        str: The name of the model corresponding to the station data, or None if not found.
    """
    table_name = f"{slug}_station"
    models = apps.get_app_config(app_label).get_models()
    for model in models:
        if table_name in model._meta.db_table:
            return model.__name__
    return None


def get_filtered_queryset(model, filters):
    filter_class = spatial_filter(model)
    filter_instance = filter_class(filters, queryset=model.objects.all())
    return filter_instance.qs
