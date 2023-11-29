from django.urls import path 
from . import views

app_name = 'coordinator'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('recruiters/', views.recruiters, name='recruiters'),
    path('recruiters/<int:id>', views.view_recruiter, name='view_recruiter'),
    path('students/', views.students, name='students'),
    path('students/<int:id>/', views.view_student, name='view_student'),
    path('messages/', views.messages, name='messages'),
]