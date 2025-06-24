from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from .forms import LoginForm, SignupForm


