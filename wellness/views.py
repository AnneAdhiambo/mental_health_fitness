from datetime import date, datetime, timedelta
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import MoodForm, JournalEntryForm, LoginForm, SignupForm, Activity, ActivityForm
from .models import Mood, JournalEntry, MoodEntry, Activity
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods  
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
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


@login_required
def add_journal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')
            content = data.get('content')

            if not date or not content:
                return JsonResponse({'success': False, 'error': 'Both date and content are required.'}, status=400)

            # Save to database
            JournalEntry.objects.create(user=request.user, date=date, content=content)

            return JsonResponse({'success': True, 'message': 'Journal saved successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

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





def get_activities(request):
    if request.method == "GET":
        activities = Activity.objects.all().values()
        return JsonResponse({"activities": list(activities)})  # Ensure JSON response
    return JsonResponse({"error": "Invalid request"}, status=400)


def add_activity(request):
    if request.method == "POST":
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX check
                data = json.loads(request.body)
                name = data.get("activity_name")
                duration = data.get("activity_duration")
                date = data.get("activity_date")

                if not name or not duration or not date:
                    return JsonResponse({"error": "Missing fields"}, status=400)

                new_activity = Activity.objects.create(name=name, duration=duration, date=date, completed=False)

                return JsonResponse({
                    "success": True,
                    "activity": {
                        "id": new_activity.id,
                        "name": new_activity.name,
                        "duration": new_activity.duration,
                        "date": str(new_activity.date),
                        "completed": new_activity.completed
                    }
                })

            else:
                # If it's a normal POST request, redirect to the same page
                return redirect("activities")

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


  
def activity_list(request):
    if request.method == "POST":
        name = request.POST.get('activity_name')
        duration = request.POST.get('activity_duration')
        date = request.POST.get('activity_date')

        if name and duration and date:
            activity = Activity.objects.create(
                name=name,
                duration=duration,
                date=date,
                completed=False
            )
            return JsonResponse({'success': True, 'id': activity.id, 'name': activity.name, 'duration': activity.duration, 'date': activity.date})
        else:
            return JsonResponse({'success': False, 'error': 'Missing fields'})

    # Get all activities
    activities = Activity.objects.all()
    return render(request, 'activity_list.html', {'activities': activities})



    


@login_required
@require_POST
def toggle_completed(request, activity_id):
    try:
        data = json.loads(request.body)
        activity = Activity.objects.get(id=activity_id, user=request.user)
        activity.completed = data.get('completed', False)
        activity.save()
        return JsonResponse({'success': True})
    except Activity.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Activity not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    
 

@login_required
def activity_stats(request):
    """View activity statistics"""
    # Get timeframe from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    start_date = date.today() - timedelta(days=days)
    
    # Base queryset
    queryset = Activity.objects.filter(user=request.user, date__gte=start_date)
    
    # Prepare statistics
    stats = {
        'total_activities': queryset.count(),
        'completed_activities': queryset.filter(completed=True).count(),
        'total_duration': sum(activity.duration for activity in queryset),
        'avg_duration': round(sum(activity.duration for activity in queryset) / max(queryset.count(), 1)),
        'days_tracked': days,
    }
    
    if stats['total_activities'] > 0:
        stats['completion_rate'] = round((stats['completed_activities'] / stats['total_activities']) * 100, 1)
    else:
        stats['completion_rate'] = 0
    
    # Daily activity counts (for charting)
    daily_data = []
    for i in range(days):
        day = date.today() - timedelta(days=i)
        day_activities = queryset.filter(date=day)
        daily_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'total': day_activities.count(),
            'completed': day_activities.filter(completed=True).count(),
            'duration': sum(activity.duration for activity in day_activities)
        })
    
    return render(request, 'activity_stats.html', {
        'stats': stats,
        'daily_data': daily_data,
        'days': days
    })


@login_required
def activities_view(request):
    if request.method == 'POST':
        activity_name = request.POST.get('activity_name')
        activity_duration = request.POST.get('activity_duration')
        activity_date = request.POST.get('activity_date')

        print("Received Data:", activity_name, activity_duration, activity_date)  # Debugging

        if activity_name and activity_duration and activity_date:
            Activity.objects.create(
                user=request.user,  # Ensure the activity is linked to the logged-in user
                name=activity_name,
                duration=int(activity_duration),
                date=activity_date
            )
            print("Activity saved!")  # Debugging
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'Invalid data'})

    activities = Activity.objects.filter(user=request.user)  # Fetch only the user's activities
    return render(request, 'activities.html', {'activities': activities})

@csrf_protect
@require_http_methods(["GET", "POST"])
def activities(request):
    if request.method == "GET":
        # Retrieve all activities, most recent first
        activities = Activity.objects.all().order_by('-date')
        return render(request, 'activities.html', {'activities': activities})
    
    elif request.method == "POST":
        try:
            # Print out all POST data for debugging
            print("Received POST data:", request.POST)

            # Get form data, using get() to prevent KeyError
            activity_name = request.POST.get('activity_name', '').strip()
            activity_duration = request.POST.get('activity_duration', '').strip()
            activity_date = request.POST.get('activity_date', '').strip()

            # Validate inputs
            if not activity_name:
                return JsonResponse({'success': False, 'error': 'Activity name is required'}, status=400)
            
            try:
                duration = int(activity_duration)
                if duration <= 0:
                    raise ValueError("Duration must be positive")
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid duration'}, status=400)

            try:
                # Try parsing date in multiple formats
                try:
                    parsed_date = datetime.strptime(activity_date, '%m/%d/%Y').date()
                except ValueError:
                    parsed_date = datetime.strptime(activity_date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date format'}, status=400)

            # Create activity
            activity = Activity.objects.create(
                name=activity_name,
                duration=duration,
                date=parsed_date,
                completed=False
            )

            return JsonResponse({
                'success': True,
                'activity': {
                    'id': activity.id,
                    'name': activity.name,
                    'duration': activity.duration,
                    'date': activity.date.strftime('%m/%d/%Y'),
                    'completed': activity.completed
                }
            }, status=201)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        
def mark_complete(request, activity_id):
    if request.method == "POST":
        activity = get_object_or_404(Activity, id=activity_id)
        activity.completed = True
        activity.save()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)


def mark_activity_complete(request, activity_id):
    if request.method == "POST":
        try:
            activity = Activity.objects.get(id=activity_id)
            activity.completed = True
            activity.save()

            return JsonResponse({"success": True, "activity_id": activity.id, "completed": True})

        except Activity.DoesNotExist:
            return JsonResponse({"success": False, "error": "Activity not found"}, status=404)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

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
