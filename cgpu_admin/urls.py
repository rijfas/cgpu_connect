from django.urls import path 
from . import views

app_name = 'cgpu_admin'

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('departments/', views.departments, name='departments'),
    path('departments/create/', views.create_department, name='create_department'),
    path('recruiters/', views.recruiters, name='recruiters'),
    path('jobs/', views.jobs, name='jobs'),
    path('shortlists/', views.shortlists, name='shortlists'),
    path('learning/', views.learning, name='learning'),
    path('announcements/', views.announcements, name='announcements'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/create/', views.create_account, name='create_account'),
    path('accounts/bulk_create/student/', views.bulk_create_student_account, name='bulk_create_student_account'),
]
