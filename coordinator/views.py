from django.shortcuts import render, redirect
from core.decorators import login_required_with_type
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .models import Coordinator
from core.models import Account, Message
from coordinator.models import Coordinator
from student.models import Student, AcademicQualification, Department, Course
from recruiter.models import Recruiter, Job, Application, Placement
from django.db.models import Count
from student.models import STREAM_CHOICE
from django.db.models import Q 

login_required_with_type('coordinator')
def register(request):
    if request.method == 'POST':
        department = Department.objects.get(id=int(request.POST['department']))
        Coordinator.objects.create(
            account=request.user,
            name=request.POST['name'],mobile_no=request.POST['mobile_no'],email_id=request.POST['email_id'],department=department)
        return redirect('coordinator:home') 
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'coordinator/register.html', context)

@login_required_with_type('coordinator')
def home(request):
    coordinator = Coordinator.objects.get(account=request.user)
    courses = [course.course for course in Course.objects.filter(department=coordinator.department)]
    jobs = Job.objects.filter(eligible_courses__course__in=courses).distinct()
    number_of_courses = Course.objects.filter(department=coordinator.department).count()
    number_of_students = Student.objects.filter(department=coordinator.department).count()
    applications = Application.objects.filter(status='CLR', student__department=coordinator.department)
    analytics = {}

    for application in applications:
        if application.job.recruiter.name not in analytics.keys():
            analytics[application.job.recruiter.name] = 1
        else:
            analytics[application.job.recruiter.name] += 1

    context = {
        'number_of_courses': number_of_courses,
        'number_of_students': number_of_students,
        'number_of_jobs': len(jobs),
        'recent_jobs': jobs.order_by('-id')[:5],
        'analytics': analytics,
    }
    return render(request, 'coordinator/home.html', context)

def profile(request):
    profile = Coordinator.objects.get(account=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'coordinator/profile.html', context)

@login_required_with_type('coordinator')
def courses(request):
    coordinator = Coordinator.objects.get(account=request.user)
    courses = Course.objects.filter(department=coordinator.department)
    context = {
        'courses': courses,
        'streams': STREAM_CHOICE,
    }
    return render(request, 'coordinator/courses.html', context)


@login_required_with_type('coordinator')
def create_course(request):
    coordinator = Coordinator.objects.get(account=request.user)
    Course.objects.create(department=coordinator.department, course=request.POST['name'], stream=request.POST['stream'])
    return redirect('coordinator:courses')

@login_required_with_type('coordinator')
def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('coordinator:courses')

@login_required_with_type('coordinator')
def jobs(request):
    coordinator = Coordinator.objects.get(account=request.user)
    search = request.GET.get('q')
    jobs = Job.objects.filter(Q(eligible_courses__department=coordinator.department) & Q(recruiter__name__icontains=search)) if search else Job.objects.filter(eligible_courses__department=coordinator.department) 
    paginator = Paginator(jobs, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'jobs': current_page.object_list,
        'total_count': jobs.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
    }
    return render(request, 'coordinator/jobs.html', context)

@login_required_with_type('coordinator')
def view_job(request, id):
    coordinator = Coordinator.objects.get(account=request.user)
    job = Job.objects.get(id=id)
    applications = Application.objects.filter(job=job, job__eligible_courses__department=coordinator.department)
    context = {
        'job': job,
        'applications': applications
    }
    return render(request, 'coordinator/view_job.html', context)

login_required_with_type('coordinator')
def applications(request):
    coordinator = Coordinator.objects.get(account=request.user)
    search = request.GET.get('q')
    applications = Application.objects.filter(Q(job__eligible_courses__department=coordinator.department) & Q(job__recruiter__name__icontains=search)) if search else Application.objects.filter(job__eligible_courses__department=coordinator.department) 
    paginator = Paginator(applications, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'applications': current_page.object_list,
        'total_count': applications.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
    }
    return render(request, 'coordinator/applications.html', context)

@login_required_with_type('coordinator')
def placements(request):
    coordinator = Coordinator.objects.get(account=request.user)
    search = request.GET.get('q')
    placements = Placement.objects.filter(Q(student__name__icontains=search)&Q(student__department=coordinator.department)) if search else Placement.objects.filter(student__department=coordinator.department) 
    paginator = Paginator(placements, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'placements': current_page.object_list,
        'total_count': placements.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
    }
    return render(request, 'coordinator/placements.html', context)

def students(request):
    search = request.GET.get('q')
    current_page_number = int(request.GET.get("page", 1))
    account = Account.objects.get(id=request.user.id)
    coordinator = Coordinator.objects.get(account=account)
    students = Student.objects.filter(first_name__icontains=search, department=coordinator.department) if search else Student.objects.filter(department=coordinator.department)
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

@login_required_with_type('coordinator')
def messages(request):
    search = request.GET.get('q')
    coordinator = Coordinator.objects.get(account=request.user)
    accounts = Student.objects.filter(Q(student__account__username__icontains=search) & Q(department=coordinator.department)) if search else Student.objects.filter(department=coordinator.department) 
    paginator = Paginator(accounts, 7)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    for account in current_page.object_list:
        account.has_new_message = Message.objects.filter(sender=account, recepient=request.user, read=False).exists()
    context = {
        'search': search,
        'students': current_page.object_list,
        'total_count': accounts.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
    }
    return render(request, 'coordinator/messages.html', context)

@login_required_with_type('coordinator')
def view_message(request, id):
    account = Account.objects.get(id=id)
    messages = Message.objects.filter(Q(sender=request.user, recepient=account) | Q(recepient=request.user, sender=account)).order_by('created_on')
    messages.filter(recepient=request.user).update(read=True)
    context = {
        'account': account,
        'messages': messages
    }
    return render(request, 'coordinator/view_message.html', context)

@login_required_with_type('coordinator')
def send_message(request, id):
    account = Account.objects.get(id=id)
    Message.objects.create(sender=request.user, recepient=account, content=request.POST['message'])

    return redirect('coordinator:view_message', id)

@login_required_with_type('coordinator')
def delete_message(request, id, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect('coordinator:view_message', id)