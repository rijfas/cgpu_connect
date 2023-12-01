from django.urls import path 
from . import views

app_name = 'coordinator'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('courses/', views.courses, name='courses'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:id>/delete/', views.delete_course, name='delete_course'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.view_job, name='view_job'),
    path('applications/', views.applications, name='applications'),
    path('students/', views.students, name='students'),
    path('students/<int:id>/', views.view_student, name='view_student'),
    path('messages/', views.messages, name='messages'),
    path('messages/<int:id>/', views.view_message, name='view_message'),
    path('messages/<int:id>/send', views.send_message, name='send_message'),
    path('messages/<int:id>/delete/<int:message_id>', views.delete_message, name='delete_message'),
]