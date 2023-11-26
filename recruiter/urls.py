from django.urls import path 
from . import views

app_name = 'recruiter'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/create/', views.create_job, name='create-job'),
    path('shortlists/', views.shortlists, name='shortlists'),
    path('messages/', views.messages, name='messages'),
]