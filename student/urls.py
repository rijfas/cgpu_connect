from django.urls import path 
from . import views

app_name = 'student'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/basic-info/', views.register_basic_info, name='register-basic-info'),
    path('register/academic-info/', views.add_academic_info, name='add-academic-info'),
    path('profile/', views.profile, name='profile'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.view_job, name='view_job'),
    path('jobs/<int:id>/apply/', views.apply_job, name='apply_job'),
    path('applications/', views.applications, name='applications'),
    path('notifications/', views.notifications, name='notifications'),
    path('learning/', views.learning, name='learning'),
]
