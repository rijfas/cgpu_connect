from django.shortcuts import render, redirect
from core.decorators import login_required_with_type
from .forms import RegisterStudentForm
from .models import Student, AcademicQualification
from django.core.exceptions import ObjectDoesNotExist

login_required_with_type('student')
def register_basic_info(request):
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        student = form.save(commit=False)
        student.account = request.user 
        if form.is_valid():
            form.save()
            return redirect('student:add-academic-info')
    form = RegisterStudentForm()
    context = {
        'form': form
    }
    return render(request, 'student/register_basic_info.html', context)

def add_academic_qualification(type, post, profile):
    board = post[f'{type}_board']
    year_of_pass = post[f'{type}_year_of_pass']
    grade = post[f'{type}_grade']
    institution = post[f'{type}_institution']
    AcademicQualification.objects.create(
        student=profile, 
        type_of_education=type.upper(),
        board=board,
        year_of_pass=year_of_pass,
        grade=grade,
        institution=institution
        )

login_required_with_type('student')
def add_academic_info(request):
    if request.method == 'POST':
        try:
            profile = Student.objects.get(account=request.user)
        except ObjectDoesNotExist:
            return redirect('student:register-basic-info')
        add_academic_qualification('hsc', request.POST, profile)
        add_academic_qualification('ssc', request.POST, profile)
        if request.POST.get("pg"):
            add_academic_qualification('ug', request.POST, profile)
        return redirect('student:home')
    return render(request, 'student/add_academic_info.html')

login_required_with_type('student')
def home(request):
    return render(request, 'student/home.html')

login_required_with_type('student')
def profile(request):
    profile = Student.objects.get(account=request.user)
    try:
        ug = AcademicQualification.objects.get(student=profile, type_of_education='UG')
    except ObjectDoesNotExist:
        ug = None
    context = {
        'profile': profile,
        'hsc': AcademicQualification.objects.get(student=profile, type_of_education='HSC'),
        'ssc': AcademicQualification.objects.get(student=profile, type_of_education='SSC'),
        'ug': ug,
    }
    return render(request, 'student/profile.html', context)

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
