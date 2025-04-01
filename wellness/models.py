from django.db import models
from django.contrib.auth.models import User


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
    activity = models.CharField(max_length=255)
    duration = models.IntegerField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity
    

class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_user = models.BooleanField(default=True)  
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        sender = "User" if self.is_user else "Bot"
        return f"{sender}: {self.content[:50]}..."
    
    class Meta:
        ordering = ['timestamp']