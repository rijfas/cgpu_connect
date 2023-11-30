from django.urls import path 
from . import views

app_name = 'cgpu_admin'

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('students/<int:id>/', views.view_student, name='view_student'),
    path('students/<int:id>/activate/', views.activate_student_account, name='activate_student_account'),
    path('students/<int:id>/deactivate/', views.deactivate_student_account, name='deactivate_student_account'),
    path('students/<int:id>/delete/', views.delete_student_account, name='delete_student_account'),
    path('students/<int:id>/change_password/', views.change_student_password, name='change_student_password'),
    path('departments/', views.departments, name='departments'),
    path('departments/<int:id>/', views.view_department, name='view_department'),
    path('departments/<int:id>/delete/', views.delete_department, name='delete_department'),
    path('departments/<int:id>/create_course/', views.create_course, name='create_course'),
    path('departments/<int:id>/delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('departments/create/', views.create_department, name='create_department'),
    path('recruiters/', views.recruiters, name='recruiters'),
    path('recruiters/<int:id>/', views.view_recruiter, name='view_recruiter'),
    path('recruiters/<int:id>/activate/', views.activate_recruiter_account, name='activate_recruiter_account'),
    path('recruiters/<int:id>/deactivate/', views.deactivate_recruiter_account, name='deactivate_recruiter_account'),
    path('recruiters/<int:id>/delete/', views.delete_recruiter_account, name='delete_recruiter_account'),
    path('recruiters/<int:id>/change_password/', views.change_recruiter_password, name='change_recruiter_password'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.view_job, name='view_job'),
    path('shortlists/', views.shortlists, name='shortlists'),
    path('shortlists/<int:id>/', views.view_shortlist, name='view_shortlist'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:id>/delete/', views.delete_announcement, name='delete_announcement'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/create/', views.create_account, name='create_account'),
    path('accounts/bulk_create/student/', views.bulk_create_student_account, name='bulk_create_student_account'),
]
