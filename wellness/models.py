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
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Journal Entry by {self.user.username} on {self.date}"
    