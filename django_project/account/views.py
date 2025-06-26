# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .forms import LoginForm, SignupForm
from .models import UserProfile, EmailVerification

def signup_view(request):
    msg = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            guest_group = Group.objects.get(name='Guests')
            user.groups.add(guest_group)
            profile = UserProfile.objects.create(user=user)

            # Create verification token
            token = EmailVerification.objects.create(
                user = user,
                email = user.email,
                expires_at = timezone.now() + timedelta(hours=24)
            )

            # send verification email
            verification_url = request.build_absolute_url(
                reverse('account:verify_email', kwargs={'token': token.token})
            )

            send_mail(
                'Verify your Dashboard account',
                f'Click this link to verify your email: {verification_url}',
                'settings.EMAIL_HOST_USER',
                [user.email],
                fail_silently=False,
            )

            return render(request, 'account/signup_success.html')
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
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                profile = UserProfile.objects.get(user=user)
                if not profile.is_email_verified:
                    return render(request, 'account/login.html', {
                        'form':form,
                        'error': 'Please verify your email before logging in'
                    })
            except UserProfile.DoesNotExist:
                pass
            login(request, user)
            return redirect('frontpage')
        else:
            msg = 'error validating form'
    else:
        form = LoginForm()

    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'account/login.html', context=context)


def verify_email(request, token):
    token_obj = get_object_or_404(EmailVerification, token=token)
    if not token_obj.is_valid(token_obj.email):
        return render(request, 'account/verification_failed.html', {
            'error': 'Token expired or invalid'
        })

    user = token_obj.user 
    user.is_active = True
    user.save()
    profile = UserProfile.objects.get(user=user)
    profile.verify_email()
    token_obj.delete()
    return render(request, 'account/verification_success.html')


def logout_view(request):
    logout(request)
    return redirect('account:login')

