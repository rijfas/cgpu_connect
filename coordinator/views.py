from django.shortcuts import render
from core.decorators import login_required_with_type

from .models import Coordinator
from core.models import Account
from student.models import Student

# Create your views here.
@login_required_with_type('coordinator')
def home(request):
    return render(request, 'coordinator/home.html', {})

def profile(request):
    return render(request, 'coordinator/profile.html', {})

def recruiters(request):
    return render(request, 'coordinator/recruiters.html', {})

def students(request):
    account = Account.objects.get(id=request.user.id)
    coordinator = Coordinator.objects.get(account=account)
    students = Student.objects.filter(section=coordinator.section)
    return render(request, 'coordinator/students.html', {'students': students})

def messages(request):
    return render(request, 'coordinator/messages.html', {})