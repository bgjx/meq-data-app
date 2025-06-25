from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings
from . models import Site

def projects(request):
    all_projects = Site.objects.all()
    return {'all_projects': all_projects}

def frontpage(request):
    context={'mapbox_access_token' : settings.MAPBOX_API_TOKEN}
    return render(request, 'frontpage/frontpage.html', context=context)
