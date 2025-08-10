from django.urls import path
from project.views.pages import pages
from project.views.api import api

app_name = 'project'

urlpatterns = [
    path('<slug:site_slug>/', pages.project_site, name='project-page'),

    path('<slug:site_slug>/download/hypo/<str:catalog_type>', pages.download_hypo_catalog, name='download-hypo-catalog'),

    path('<slug:site_slug>/download/picking/', pages.download_picking_catalog, name='download-picking-catalog'),

    path('<slug:site_slug>/download/station/', pages.download_station, name='download-station'),

    path('<slug:site_slug>/upload/', pages.upload_form, name='upload-form'),

    path('<slug:site_slug>/general-performance', pages.general_performance, name='general-performance'),

    path('<slug:site_slug>/detail-analytics', pages.detail_analytics, name='detail-analytics'),

    # API URL
    path('api/general-performance/<slug:site_slug>', api.GeneralPerformanceAPIView.as_view(), name='api-general-performance'),
]