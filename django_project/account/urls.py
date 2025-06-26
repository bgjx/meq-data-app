from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<uuid:token>', views.verify_email, name='verify_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name = 'account/password_reset_form.html',
        email_template_name = 'account/password_reset_email.html',
        subject_template_name = 'account/password_reset_subject.txt'
        ), name = 'password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'account/password_reset_done.html'
        ), name='password_reset_done'),
    path('reset/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ), name='password_reset_complete'),
]
