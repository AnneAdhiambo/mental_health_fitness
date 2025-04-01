from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.timezone import now


class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mood_type} - {self.user.username}'


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"Journal Entry by {self.user.username} on {self.date}"


class MoodEntry(models.Model):
    mood = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mood
   

class Activity(models.Model):
    name = models.CharField(max_length=255, default="Unnamed Activity")  
    duration = models.IntegerField()  # duration in minutes
    date = models.DateField(default=now)  # Set a default value
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow NULL

    def __str__(self):
        return f"{self.name} ({self.duration} min) on {self.date}"