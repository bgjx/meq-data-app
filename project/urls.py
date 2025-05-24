from django.urls import path
from . import views

urlpatterns = [
    path('<slug:site_slug>/', views.project_site, name='project-page'),

    path('<slug:site_slug>/download/csv/wcc', views.download_csv_wcc, name='download-wcc'),

    path('<slug:site_slug>/download/csv/nll', views.download_csv_nll, name='download-nll'),

    path('<slug:site_slug>/maps', views.meq_maps, name='meq-maps'),

    path('<slug:site_slug>/get-meq-data', views.get_meq_data, name='get-meq-data'),

]