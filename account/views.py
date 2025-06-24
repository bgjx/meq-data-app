from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import LoginForm, SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            guest_group = Group.objects.get(name='Guests')
            user.groups.add(guest_group)
    else:
        form = SignupForm()
    context = {
        'form':form
    }
    return render(request, 'account/signup.html', context=context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('frontpage:')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('account:login')

