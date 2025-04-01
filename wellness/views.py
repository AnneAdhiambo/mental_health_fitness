import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import MoodForm, JournalEntryForm, LoginForm, SignupForm, Activity, ActivityForm
from .models import Mood, JournalEntry, MoodEntry, Activity
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Conversation, Message
from .gemini_client import GeminiClient


def home(request):
    return render(request, 'home.html')


def activities(request):
    return render(request, 'activities.html')


@login_required
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


@login_required
def journal(request):
    if request.method == 'GET':
        entries = JournalEntry.objects.filter(user=request.user).order_by('-date')
        return render(request, 'journal.html', {'entries': entries})



def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')  # Redirect after successful signup
    else:
        form = SignupForm()  # Initialize an empty form for GET requests

    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    return render(request, 'logout.html')


import logging

logger = logging.getLogger(__name__)



@login_required
def save_journal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')
            content = data.get('content')

            if not date or not content:
                return JsonResponse({'error': 'Both date and content are required.'}, status=400)

            JournalEntry.objects.create(user=request.user, date=date, content=content)
            return JsonResponse({'message': 'Journal saved successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def save_mood(request):
    if request.method == 'POST':
        mood_type = request.POST.get('mood')  # Get the mood type
        description = request.POST.get('notes', '')  # Get optional notes
        user = request.user  # The logged-in user

        if mood_type:
            # Create and save the new mood entry
            mood = Mood(user=user, mood_type=mood_type, description=description)
            mood.save()

            # Return a success message or the saved data
            return JsonResponse({'success': True, 'message': 'Mood saved successfully!'})

        return JsonResponse({'success': False, 'message': 'Mood type is required'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})



@login_required
def get_journal_entries(request):
    try:
        entries = JournalEntry.objects.filter(user=request.user).values('date', 'content')
        return JsonResponse(list(entries), safe=False)
    except Exception as e:
        logger.error(f"Error fetching journal entries: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def mood_tracker(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mood_tracker')  # Redirect to the same page after saving
    else:
        form = MoodForm()
    
    # Fetch mood history from the database
    mood_entries = MoodEntry.objects.all().order_by('-date')  # Order by most recent

    return render(request, 'mood_tracker.html', {
        'form': form,
        'mood_entries': mood_entries,
    })
def save_mood_entry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mood = data.get('mood')
            notes = data.get('notes')
            
            # Save to the database
            MoodEntry.objects.create(mood=mood, notes=notes)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def add_activity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            activity_text = data.get('activity')
            duration = data.get('duration')

            # Save to database
            activity = Activity.objects.create(activity=activity_text, duration=duration)
            return JsonResponse({
                'success': True,
                'activity': {
                    'id': activity.id,
                    'activity': activity.activity,
                    'duration': activity.duration,
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def toggle_completed(request, activity_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            completed = data.get('completed', False)
            activity = Activity.objects.get(id=activity_id)
            activity.completed = completed
            activity.save()
            return JsonResponse({'success': True})
        except Activity.DoesNotExist:
            return JsonResponse({'error': 'Activity not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'activity_tracker.html', {'activities': activities})

def activities_view(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    activities = Activity.objects.all()
    form = ActivityForm()
    return render(request, 'activities.html', {'form': form, 'activities': activities})

def chat_view(request):
 
    if 'conversation_id' not in request.session:
        conversation = Conversation.objects.create()
        request.session['conversation_id'] = conversation.id
    else:
        conversation = Conversation.objects.get(id=request.session['conversation_id'])
    messages = conversation.messages.all()
    
    return render(request, 'chat_view.html', {'messages': messages})

def send_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        conversation_id = request.session.get('conversation_id')
        
        if not conversation_id:
            conversation = Conversation.objects.create()
            request.session['conversation_id'] = conversation.id
        else:
            conversation = Conversation.objects.get(id=conversation_id)
        
        Message.objects.create(
            conversation=conversation,
            content=user_message,
            is_user=True
        )

        messages = conversation.messages.all()
        client = GeminiClient()
        bot_response = client.get_chat_response(messages)
        

        bot_message = Message.objects.create(
            conversation=conversation,
            content=bot_response,
            is_user=False
        )
        
        return JsonResponse({
            'message': bot_response,
            'timestamp': bot_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def new_conversation(request):
    conversation = Conversation.objects.create()
    request.session['conversation_id'] = conversation.id
    return redirect('chat')