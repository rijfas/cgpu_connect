from django.shortcuts import render
from student.models import Department, Student
from core.decorators import login_required_with_type


@login_required_with_type('admin')
def home(request):
    return render(request, 'cgpu_admin/home.html')

@login_required_with_type('admin')
def students(request):
    return render(request, 'cgpu_admin/students.html')

@login_required_with_type('admin')
def departments(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'cgpu_admin/departments.html', context)

@login_required_with_type('admin')
def recruiters(request):
    return render(request, 'cgpu_admin/recruiters.html')

@login_required_with_type('admin')
def jobs(request):
    return render(request, 'cgpu_admin/jobs.html')

@login_required_with_type('admin')
def shortlists(request):
    return render(request, 'cgpu_admin/shortlists.html')

@login_required_with_type('admin')
def learning(request):
    return render(request, 'cgpu_admin/learning.html')

@login_required_with_type('admin')
def announcements(request):
    return render(request, 'cgpu_admin/announcements.html')

@login_required_with_type('admin')
def accounts(request):
    return render(request, 'cgpu_admin/accounts.html')


