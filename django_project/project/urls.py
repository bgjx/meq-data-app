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
    path('api/hypocenter-table-data/<slug:site_slug>/<str:catalog_type>', api.HypocenterTableDataAPIView.as_view(), name='api-hypocenter-table-data'),

    path('api/picking-table-data/<slug:site_slug>', api.PickingTableDataAPIView.as_view(), name='api-picking-table-data'),

    path('api/station-table-data/<slug:site_slug>', api.StationTableDataAPIView.as_view(), name='api-station-table-data'),

    path('api/general-performance/<slug:site_slug>', api.GeneralPerformanceAPIView.as_view(), name='api-general-performance'),

    path('api/detail-analytics/<slug:site_slug>', api.DetailAnalyticsAPIView.as_view(), name='api-detail-analytics')
]