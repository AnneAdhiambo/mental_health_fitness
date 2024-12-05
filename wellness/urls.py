from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from.forms import LoginForm



urlpatterns = [
    path('', views.home, name='home'),
    path('mood_tracker/', views.mood_tracker, name='mood_tracker'),
    path('journal/', views.journal, name='journal'),
    path('activities/', views.activities, name='activities'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

]