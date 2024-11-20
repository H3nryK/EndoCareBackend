from django.db import models

class UserProfile(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_picture = models.URLField(null=True, blank=True)
    next_period = models.CharField(max_length=50, default="Not set")
    cycle_length = models.CharField(max_length=50, default="Not set")
    last_period = models.CharField(max_length=50, default="Not set")
    tracked_cycles = models.IntegerField(default=0)
    logged_symptoms = models.IntegerField(default=0)

    def __str__(self):
        return self.email
