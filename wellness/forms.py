from django import forms
from .models import Mood, JournalEntry, Activity
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood_type', 'description']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'duration', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity Name'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (minutes)'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['content']


class LoginForm(AuthenticationForm):
         username = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Your Username',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))
password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))