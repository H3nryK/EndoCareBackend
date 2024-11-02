from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class CustomUser(AbstractUser):
    firebase_uid = models.CharField(max_length=128, unique=True)
    profile_picture = models.URLField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    next_period = models.DateField(null=True, blank=True)
    cycle_length = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True
    )
    last_period = models.DateField(null=True, blank=True)
    tracked_cycles = models.PositiveIntegerField(default=0)
    logged_symptoms = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email}'s Profile"