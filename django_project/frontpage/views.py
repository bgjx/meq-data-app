from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse


from frontpage.models import Site
from frontpage.decorators import guest_or_admin_required
from project.models import Updates
from frontpage.utils import get_updates

import csv


def projects(request):
    all_projects = Site.objects.all()
    return {'all_projects': all_projects}

@login_required
@guest_or_admin_required
def frontpage(request):
    # Query new updates
    latest_updates = Updates.objects.order_by('-updated_at')[:5]

    context={
        'mapbox_access_token' : settings.MAPBOX_API_TOKEN,
        'latest_updates': latest_updates
    }
    
    return render(request, 'frontpage/frontpage.html', context=context)

def download_updates(request):
    # Get model name
    model = get_updates('project')
    
    # Get reference model
    get_model = apps.get_model('project', model)

    # Http response
    response = HttpResponse(
        content_type = "text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="updates_download.csv" '}
    )

    # Write header
    writer = csv.writer(response, lineterminator='\n')
    headers = [field.name for field in get_model._meta.fields[1:]]
    writer.writerow(headers)

    # writing data
    for data in get_model.objects.values(*headers).iterator():
        writer.writerow([data[header] for header in headers])

    return response
