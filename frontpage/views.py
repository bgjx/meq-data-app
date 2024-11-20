from django.shortcuts import render
from django.shortcuts import get_object_or_404
from . models import Site


def frontpage(request):
    all_sites = Site.objects.all()
    context = {'all_sites': all_sites}
    context['mapbox_access_token'] = 'pk.eyJ1IjoiZWRlbG8iLCJhIjoiY20zNG1zN3F5MDFjdzJsb3N4ZDJ1ZTR1byJ9.bgl0vpixXnhDKJ8SnW4PYA'
    return render(request, 'frontpage/frontpage.html', context=context)


def list_project(request, site_slug = None):
    site = get_object_or_404(Site, slug=site_slug)
    context = {'site': site}
    return render(request, 'project/site-analytics.html', context)