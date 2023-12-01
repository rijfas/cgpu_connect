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
    path('applications/<int:id>/', views.view_application, name='view_application'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.messages, name='messages'),
    path('results/add/', views.add_result, name='add_result'),
    path('results/<int:id>/delete/', views.delete_result, name='delete_result'),
    path('messages/send/', views.send_message, name='send_message'),
    path('messages/<int:id>/delete/', views.delete_message, name='delete_message'),
]
