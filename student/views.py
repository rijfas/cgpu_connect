from django.shortcuts import render, redirect
from core.decorators import login_required_with_type
from .forms import RegisterStudentForm


login_required_with_type('student')
def register_basic_info(request):
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        student = form.save(commit=False)
        student.account = request.user 
        if form.is_valid():
            form.save()
            return redirect('student:home')
    form = RegisterStudentForm()
    context = {
        'form': form
    }
    return render(request, 'student/register_basic_info.html', context)

login_required_with_type('student')
def add_academic_info(request):
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        student = form.save(commit=False)
        student.account = request.user 
        if form.is_valid():
            form.save()
            return redirect('student:home')
    form = RegisterStudentForm()
    context = {
        'form': form
    }
    return render(request, 'student/register.html', context)

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
