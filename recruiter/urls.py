from django.urls import path 
from . import views

app_name = 'recruiter'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.view_job, name='view_job'),
    path('jobs/<int:id>/shortlist/', views.view_shortlist, name='view_shortlist'),
    path('jobs/<int:id>/shortlist/add/', views.add_to_shortlist, name='add_to_shortlist'),
    path('jobs/<int:id>/shortlist/remove/', views.remove_from_shortlist, name='remove_from_shortlist'),
    path('jobs/<int:id>/shortlist/publish/', views.publish_shortlist, name='publish_shortlist'),
    path('jobs/create/', views.create_job, name='create-job'),
    path('shortlists/', views.shortlists, name='shortlists'),
    path('messages/', views.messages, name='messages'),
]