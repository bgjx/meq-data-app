from django.urls import path
from . import views

urlpatterns = [
    path('<slug:site_slug>/', views.project_site, name='project-page'),

    path('<slug:site_slug>/download/<str:catalog_type>', views.download_catalog, name='download-catalog'),

    path('<slug:site_slug>/maps', views.meq_maps, name='meq-maps'),

    path('<slug:site_slug>/get-meq-data', views.get_meq_data, name='get-meq-data'),

    path('<slug:site_slug>/data-analysis', views.data_analysis, name='data-analysis'),

    path('<slug:site_slug>/get-data-analysis', views.get_data_analysis, name='get-data-analysis'),

]