from django.shortcuts import render, redirect
from core.decorators import login_required_with_type
from .forms import RegisterStudentForm
from .models import Student, AcademicQualification, SEMESTER_CHOICES, Result
from core.models import Account, Message
from django.db.models import Q
from cgpu_admin.models import Announcement
from recruiter.models import Job, Application
from django.core.exceptions import ObjectDoesNotExist
from coordinator.models import Coordinator

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
    student = Student.objects.get(account=request.user)
    jobs = Job.objects.filter(eligible_courses=student.course).order_by('-id')[:3]
    announcements = Announcement.objects.all().order_by('-id')[:10]
    context = {
        'jobs': jobs,
        'announcements': announcements
    }
    return render(request, 'student/home.html', context)

login_required_with_type('student')
def profile(request):
    profile = Student.objects.get(account=request.user)
    results = Result.objects.filter(student=profile)
    try:
        ug = AcademicQualification.objects.get(student=profile, type_of_education='UG')
    except ObjectDoesNotExist:
        ug = None
    context = {
        'profile': profile,
        'hsc': AcademicQualification.objects.get(student=profile, type_of_education='HSC'),
        'ssc': AcademicQualification.objects.get(student=profile, type_of_education='SSC'),
        'ug': ug,
        'semesters': SEMESTER_CHOICES,
        'results': results
    }
    return render(request, 'student/profile.html', context)

login_required_with_type('student')
def add_result(request):
    student = Student.objects.get(account=request.user)
    Result.objects.create(student=student, semester=request.POST['semester'], gpa=request.POST['grade'], is_failed=True if request.POST.get('passed') else False)
    return redirect('student:profile')

login_required_with_type('student')
def delete_result(request, id):
    result = Result.objects.get(id=id)
    result.delete()
    return redirect('student:profile')

login_required_with_type('student')
def jobs(request):
    student = Student.objects.get(account=request.user)
    jobs = Job.objects.filter(eligible_courses=student.course)
    applied_jobs = [application.job for application in Application.objects.filter(student=student)]
    for job in jobs:
        if job in applied_jobs:
            job.is_already_applied = True 
        else:
            job.is_already_applied = False

    context = {
        'jobs': jobs
    }
    return render(request, 'student/jobs.html', context)

login_required_with_type('student')
def view_job(request, id):
    student = Student.objects.get(account=request.user)
    job = Job.objects.get(id=id)
    try:
        application = Application.objects.get(job=job, student=student)
        job.is_already_applied = True
    except ObjectDoesNotExist:
        application = None
        job.is_already_applied = False
    context = {
        'job': job,
        'application': application,
    }
    return render(request, 'student/view_job.html', context)

login_required_with_type('student')
def apply_job(request, id):
    student = Student.objects.get(account=request.user)
    job = Job.objects.get(id=id)
    Application.objects.create(job=job, student=student)
    return redirect('student:jobs')

login_required_with_type('student')
def applications(request):
    student = Student.objects.get(account=request.user)
    applications = Application.objects.filter(student=student)
    context = {
        'applications': applications
    }
    return render(request, 'student/applications.html', context)

login_required_with_type('student')
def view_application(request, id):
    application = Application.objects.get(id=id)
    context = {
        'application': application
    }
    return render(request, 'student/view_application.html', context)

login_required_with_type('student')
def notifications(request):
    announcements = Announcement.objects.all()
    context = {
        'announcements': announcements
    }
    return render(request, 'student/notifications.html', context)

login_required_with_type('student')
def messages(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(recepient=request.user)).order_by('created_on')
    messages.filter(recepient=request.user).update(read=True)
    context = {
        'messages': messages
    }
    return render(request, 'student/messages.html', context)


@login_required_with_type('student')
def send_message(request):
    student = Student.objects.get(account=request.user)
    coordinator = Coordinator.objects.get(department=student.department)
    Message.objects.create(sender=request.user, recepient=coordinator.account, content=request.POST['message'])

    return redirect('student:messages')

@login_required_with_type('student')
def delete_message(request, id):
    message = Message.objects.get(id=id)
    message.delete()
    return redirect('student:messages')
