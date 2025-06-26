from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from . models import Site

def is_admin(user):
    return user.groups.filter(name='Admins').exists()

def is_guest_or_admin(user):
    return user.groups.filter(name__in=['Guests', 'Admins']).exist()

def projects(request):
    all_projects = Site.objects.all()
    return {'all_projects': all_projects}

@login_required
@user_passes_test(is_guest_or_admin)
def frontpage(request):
    context={'mapbox_access_token' : settings.MAPBOX_API_TOKEN}
    return render(request, 'frontpage/frontpage.html', context=context)