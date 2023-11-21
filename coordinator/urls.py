from django.urls import path 
from . import views

app_name = 'coordinator'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('jobs/', views.recruiters, name='recruiters'),
    path('shortlists/', views.students, name='students'),
    path('messages/', views.messages, name='messages'),
]