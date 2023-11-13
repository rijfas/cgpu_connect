from django.shortcuts import render
from student.models import Department, Student
from core.decorators import admin_login_required

@admin_login_required
def home(request):
    return render(request, 'cgpu_admin/home.html')

@admin_login_required
def students(request):
    return render(request, 'cgpu_admin/students.html')

@admin_login_required
def departments(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'cgpu_admin/departments.html', context)

@admin_login_required
def recruiters(request):
    return render(request, 'cgpu_admin/recruiters.html')

@admin_login_required
def jobs(request):
    return render(request, 'cgpu_admin/jobs.html')

@admin_login_required
def shortlists(request):
    return render(request, 'cgpu_admin/shortlists.html')

@admin_login_required
def learning(request):
    return render(request, 'cgpu_admin/learning.html')

@admin_login_required
def announcements(request):
    return render(request, 'cgpu_admin/announcements.html')

@admin_login_required
def accounts(request):
    return render(request, 'cgpu_admin/accounts.html')


