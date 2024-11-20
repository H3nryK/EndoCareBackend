from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    firebase_uid = models.CharField(max_length=128, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email