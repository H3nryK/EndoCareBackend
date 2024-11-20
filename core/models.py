from django.db import models
from django.utils.timezone import timedelta

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

    def save(self, *args, **kwargs):
        if self.last_period and self.cycle_length:
            self.next_period = self.last_period + timedelta(days=self.cycle_length)
        super().save(*args, **kwargs)

class Medication(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    notify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.dosage}"

class Appointment(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    date = models.DateField()
    notify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date}"