from django.urls import path 
from . import views

app_name = 'student'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('jobs/', views.jobs, name='jobs'),
    path('applications/', views.applications, name='applications'),
    path('notifications/', views.notifications, name='notifications'),
    path('learning/', views.learning, name='learning'),
]
