from django.urls import path
from .views import AnalysisDataAPIView
from . import views

app_name = 'project'

urlpatterns = [
    path('<slug:site_slug>/', views.project_site, name='project-page'),

    path('<slug:site_slug>/download/hypo/<str:catalog_type>', views.download_hypo_catalog, name='download-hypo-catalog'),

    path('<slug:site_slug>/download/picking/', views.download_picking_catalog, name='download-picking-catalog'),

    path('<slug:site_slug>/download/station/', views.download_station, name='download-station'),

    path('<slug:site_slug>/upload/', views.upload_form, name='upload-form'),
    # path('<slug:site_slug>/maps', views.meq_maps, name='meq-maps'),

    # path('<slug:site_slug>/get-meq-data', views.get_meq_data, name='get-meq-data'),

    path('<slug:site_slug>/data-analysis', views.data_analysis, name='data-analysis'),

    path('api/analysis/<slug:site_slug>', AnalysisDataAPIView.as_view(), name='analysis-data'),
]