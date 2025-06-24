from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import LoginForm, SignupForm

def signup_view(request):
    msg = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'guest created'
            guest_group = Group.objects.get(name='Guests')
            user.groups.add(guest_group)
            return redirect('login')
        else:
            msg = 'form is not valid'
    else:
        form = SignupForm()
    context = {
        'form':form,
        'msg': msg
    }
    return render(request, 'account/signup.html', context=context)


def login_view(request):
    msg = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username  = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('frontpage')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    else:
        form = LoginForm()
    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'account/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('account:login')

