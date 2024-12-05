from django.contrib import admin
from .models import JournalEntry, Mood

# Register each model separately
admin.site.register(JournalEntry)
admin.site.register(Mood)
