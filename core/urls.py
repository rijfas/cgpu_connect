from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
     path('login/', views.login, name='login'),
     path('change-password/', views.change_password, name='change_password'),
]
