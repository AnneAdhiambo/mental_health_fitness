from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from.forms import LoginForm
from .views import toggle_completed




urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Mood Tracker
    path('mood_tracker/', views.mood_tracker, name='mood_tracker'),
    path('save-mood/', views.save_mood, name='save_mood'),
    path('save-mood-entry/', views.save_mood_entry, name='save_mood_entry'),

    # Journal
    path('journal/', views.journal, name='journal'),
    path('save-journal/', views.save_journal, name='save_journal'),
    path('get-journal-entries/',views.get_journal_entries, name='get_journal_entries'),
    path('journal/add/',views.add_journal, name='add_journal'),




    # activities
    path('activities/', views.activities_view, name='activities_view'),
    path('activities/', views.activities_view, name='activities_list'),
    path('add-activity/', views.add_activity, name='add_activity'),
    path('toggle-completed/<int:activity_id>/', views.toggle_completed, name='toggle_completed'),
    path('delete-activity/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('activity-list/', views.activity_list, name='activity_list'),
    path('activity-stats/', views.activity_stats, name='activity_stats'),
    path('activities/add-activity/', views.add_activity, name='add_activity'),  # Make sure this exists
    path("activities/delete/<int:activity_id>/", views.delete_activity, name="delete_activity"),
    path("activities/complete/<int:activity_id>/", views.mark_activity_complete, name="mark_activity_complete"),
    path("activities/mark-complete/<int:activity_id>/", views.mark_complete, name="mark_complete"),


    


    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),



    # path('chat/', views.chat, name='chat'),  # Creating a new chat
    # path("chatbot/", views.chatbot, name="chatbot"),  # View chatbot UI
    
    # path('chat/<int:conversation_id>/', views.conversation, name='conversation'),
    
    # path('chatbot/send_message/', views.send_message, name='send_message'),
    
    # path('chat/<int:conversation_id>/update-title/', views.update_conversation_title, name='update_conversation_title'),
    
    # path('chat/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
]