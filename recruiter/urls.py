from django.urls import path 
from . import views

app_name = 'recruiter'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.view_job, name='view_job'),
    path('jobs/create/', views.create_job, name='create-job'),
    path('applications/', views.applications, name='applications'),
    path('applications/<int:id>/', views.view_application, name='view_application'),
    path('shortlists/', views.shortlists, name='shortlists'),
    path('shortlists/create/', views.create_shortlist, name='create_shortlist'),
    path('shortlists/<int:id>/', views.view_shortlist, name='view_shortlist'),
    path('shortlists/<int:id>/delete/', views.delete_shortlist, name='delete_shortlist'),
    path('shortlists/<int:id>/add/<int:application_id>/', views.add_to_shortlist, name='add_to_shortlist'),
    path('shortlists/<int:id>/remove/<int:application_id>/', views.remove_from_shortlist, name='remove_from_shortlist'),
    path('shortlists/<int:id>/publish/', views.publish_shortlist, name='publish_shortlist'),
    path('messages/', views.messages, name='messages'),
    path('messages/send/', views.send_message, name='send_message'),
    path('messages/<int:id>/delete/', views.delete_message, name='delete_message'),
]