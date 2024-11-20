from django.urls import path
from . import views

urlpatterns = [
    path('<slug:site_slug>/', views.project_site, name='project-page'),
]