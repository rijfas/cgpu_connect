from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.forms import AuthenticationForm
from student.models import Student
from django.core.exceptions import ObjectDoesNotExist
def login(request):
    if request.POST:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login_user(request, user)
            if user.type == 'admin':
                return redirect('cgpu_admin:home')
            elif user.type == 'student':
                try:
                    profile = Student.objects.get(account=request.user)
                except ObjectDoesNotExist:
                    return redirect('student:register-basic-info')
                return redirect('student:home')
        else:
            form = AuthenticationForm(request, request.POST)
            return render(request, 'registration/login.html', {"form": form})

    form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form})
