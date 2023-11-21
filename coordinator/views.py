from django.shortcuts import render
from core.decorators import login_required_with_type

# Create your views here.
@login_required_with_type('coordinator')
def home(request):
    return render(request, 'coordinator/home.html', {})

def profile(request):
    return render(request, 'coordinator/profile.html', {})

def recruiters(request):
    return render(request, 'coordinator/recruiters.html', {})

def students(request):
    return render(request, 'coordinator/students.html', {})

def messages(request):
    return render(request, 'coordinator/messages.html', {})