from django.urls import path 
from . import views

app_name = 'cgpu_admin'

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('departments/', views.departments, name='departments'),
    path('recruiters/', views.recruiters, name='recruiters'),
    path('jobs/', views.jobs, name='jobs'),
    path('shortlists/', views.shortlists, name='shortlists'),
    path('learning/', views.learning, name='learning'),
    path('announcements/', views.announcements, name='announcements'),
    path('accounts/', views.accounts, name='accounts'),
]
