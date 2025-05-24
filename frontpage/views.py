from django.shortcuts import render
from django.shortcuts import get_object_or_404
from . models import Site


def projects(request):
    all_projects = Site.objects.all()
    return {'all_projects': all_projects}

def frontpage(request):
    context={'mapbox_access_token' :'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'}
    return render(request, 'frontpage/frontpage.html', context=context)
