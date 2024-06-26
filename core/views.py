from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.forms import AuthenticationForm
from student.models import Student, AcademicQualification
from recruiter.models import Recruiter
from coordinator.models import Coordinator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def login(request):
    if request.POST:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login_user(request, user)
            if user.type == 'admin':
                return redirect('cgpu_admin:home')
            elif user.type == 'student':
                if not Student.objects.filter(account=request.user).exists():
                    return redirect('student:register-basic-info')
                if not AcademicQualification.objects.filter(student=Student.objects.get(account=request.user)).exists():
                    return redirect('student:add-academic-info')
                return redirect('student:home')
            elif user.type == 'recruiter':
                if not Recruiter.objects.filter(account=request.user).exists():
                    return redirect('recruiter:register')
                return redirect('recruiter:home')
            elif user.type == 'coordinator':
                if not Coordinator.objects.filter(account=request.user).exists():
                    return redirect('coordinator:register')
                return redirect('coordinator:home')

        else:
            form = AuthenticationForm(request, request.POST)
            return render(request, 'registration/login.html', {"form": form})

    form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form})

@login_required
def home(request):
    if request.user.type == 'admin':
        return redirect('cgpu_admin:home')
    elif request.user.type == 'student':
        if not Student.objects.filter(account=request.user).exists():
            return redirect('student:register-basic-info')
        if not AcademicQualification.objects.filter(student=Student.objects.get(account=request.user)).exists():
            return redirect('student:add-academic-info')
        return redirect('student:home')
    elif request.user.type == 'recruiter':
        if not Recruiter.objects.filter(account=request.user).exists():
            return redirect('recruiter:register')
        return redirect('recruiter:home')
    elif request.user.type == 'coordinator':
        if not Coordinator.objects.filter(account=request.user).exists():
            return redirect('coordinator:register')
        return redirect('coordinator:home')
    

@login_required
def change_password(request):
    account = request.user
    account.password = make_password(request.POST['password'])
    account.save()
    return redirect('core:login')
