from django.shortcuts import render
from core.decorators import login_required_with_type
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .models import Coordinator
from core.models import Account
from student.models import Student, AcademicQualification
from recruiter.models import Recruiter, Job

# Create your views here.
@login_required_with_type('coordinator')
def home(request):
    return render(request, 'coordinator/home.html', {})

def profile(request):
    return render(request, 'coordinator/profile.html', {})

@login_required_with_type('coordinator')
def recruiters(request):
    search = request.GET.get('q')
    recruiters = Recruiter.objects.filter(name__icontains=search) if search else Recruiter.objects.all() 
    paginator = Paginator(recruiters, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'recruiters': current_page.object_list,
        'total_count': recruiters.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
    }
    return render(request, 'coordinator/recruiters.html', context)

@login_required_with_type('coordinator')
def view_recruiter(request, id):
    recruiter = Recruiter.objects.get(id=id)
    jobs = Job.objects.filter(recruiter=recruiter)

    context = {
        'recruiter': recruiter,
        'jobs': jobs
    }

    return render(request, 'coordinator/view_recruiter.html', context)

def students(request):
    search = request.GET.get('q')
    current_page_number = int(request.GET.get("page", 1))
    account = Account.objects.get(id=request.user.id)
    coordinator = Coordinator.objects.get(account=account)
    students = Student.objects.filter(first_name__icontains=search, course=coordinator.course) if search else Student.objects.filter(course=coordinator.course)
    paginator = Paginator(students, 11)
    current_page = paginator.page(current_page_number)
    return render(request, 'coordinator/students.html', {
        'search': search,
        'students': current_page.object_list,
        'total_count': students.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
        })

@login_required_with_type('coordinator')
def view_student(request, id):
    student = Student.objects.get(id=id)
    try:
        ug = AcademicQualification.objects.get(student=student, type_of_education='UG')
    except ObjectDoesNotExist:
        ug = None
    context = {
        'student': student,
        'hsc': AcademicQualification.objects.get(student=student, type_of_education='HSC'),
        'ssc': AcademicQualification.objects.get(student=student, type_of_education='SSC'),
        'ug': ug,
    }
    return render(request, 'coordinator/view_student.html', context)

def messages(request):
    return render(request, 'coordinator/messages.html', {})