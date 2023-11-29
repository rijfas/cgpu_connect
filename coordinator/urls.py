from django.urls import path 
from . import views

app_name = 'coordinator'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('recruiters/', views.recruiters, name='recruiters'),
    path('students/', views.students, name='students'),
    path('messages/', views.messages, name='messages'),
]