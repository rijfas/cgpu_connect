from django.shortcuts import render
from core.decorators import login_required_with_type

login_required_with_type('student')
def home(request):
    return render(request, 'student/home.html')

login_required_with_type('student')
def profile(request):
    return render(request, 'student/profile.html')

login_required_with_type('student')
def jobs(request):
    return render(request, 'student/jobs.html')

login_required_with_type('student')
def applications(request):
    return render(request, 'student/applications.html')

login_required_with_type('student')
def notifications(request):
    return render(request, 'student/notifications.html')

login_required_with_type('student')
def learning(request):
    return render(request, 'student/learning.html')
