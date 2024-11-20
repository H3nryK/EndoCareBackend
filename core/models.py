from django.db import models
from django.utils.timezone import timedelta

class UserProfile(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_picture = models.URLField(null=True, blank=True)
    next_period = models.FloatField()
    cycle_length = models.FloatField()
    last_period = models.FloatField()
    tracked_cycles = models.IntegerField(default=0)
    logged_symptoms = models.IntegerField(default=0)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.last_period and self.cycle_length:
            self.next_period = self.last_period + timedelta(days=float(self.cycle_length))
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

class Periods(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='periods')
    start_date = models.DateField()
    cycle_length = models.FloatField()
    period_duration = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Periods for {self.user_profile.name} on {self.start_date}"
    
class EndoBot(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='endo_bot', null=True, blank=True)
    bot = models.CharField(max_length=200, default="EndoBot", null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"EndoBot message for {self.message} on {self.created_at}"
    
class Quizes(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='quizes')
    quiz_name = models.CharField(max_length=200)
    quiz_score = models.IntegerField()
    quiz_answers = models.JSONField(default=list, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quiz for {self.user_profile.name} on {self.quiz_name}"
    
class Stories(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='stories')
    story_title = models.CharField(max_length=200)
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Story for {self.user_profile.name} on {self.story_title}"

class Symptom(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='symptoms')
    symptom_name = models.CharField(max_length=200)
    symptom_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Symptom for {self.user_profile.name} on {self.symptom_name}"