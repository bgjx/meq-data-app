from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from frontpage.models import Site
from project.models import Updates
from frontpage.decorators import guest_or_admin_required

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