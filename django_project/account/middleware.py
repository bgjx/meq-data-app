from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('login'),
            reverse('signup'),
            reverse('logout'),
            '/account/verify',
            '/account/password_reset',
            '/account/password_reset/done/',
            '/account/reset/',
            '/account/reset/done/',
            '/static/'
        ]
    
    def __call__(self, request):
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in self.exempt_urls):
            return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response