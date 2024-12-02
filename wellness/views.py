from django.shortcuts import render, redirect
from .forms import MoodForm, JournalEntryForm, LoginForm, SignupForm
from .models import Mood, JournalEntry
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request, 'home.html')



def activities(request):
    return render(request, 'activities.html')


def mood_tracker(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            return redirect('home')
    else:
        form = MoodForm()
    moods = Mood.objects.filter(user=request.user)
    return render(request, 'mood_tracker.html', {'form': form, 'moods': moods})


def journal(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('home')
    else:
        form = JournalEntryForm()
    entries = JournalEntry.objects.filter(user=request.user)
    return render(request, 'journal.html', {'form': form, 'entries': entries})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')  # Redirect after successful signup
    else:
        form = SignupForm()  # Initialize an empty form for GET requests

    return render(request, 'signup.html', {
        'form': form  # Pass the form to the template
    })


def logout(request):
    return render(request, 'logout')
