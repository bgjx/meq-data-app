from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone   
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified_at= models.DateTimeField(null=True, blank=True)
    organization = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def is_email_verified(self):
        return self.email_verified_at is not None 
    
    def verify_email(self):
        self.email_verified_at = timezone.now()
        self.save()


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=2555)
    token = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now())
    expires_at = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=1))
    
    def __str__(self):
        return f"Verification for {self.user.email}"
    
    def is_valid(self, email: str):
        return (
            self.email == email 
            and self.expires_at > timezone.now()
        )