from django.urls import path

from . import views

urlpatterns = [
    # main page url
    path('', views.frontpage, name='frontpage'),
    path('download-updates', views.download_updates, name='download-updates')
]
