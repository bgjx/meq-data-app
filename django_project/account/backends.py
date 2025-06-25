from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User 
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None 
