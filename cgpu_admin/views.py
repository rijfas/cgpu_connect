from django.shortcuts import render, redirect
from core.models import Account, Message
from django.core.exceptions import ObjectDoesNotExist
from student.models import Student, Department, AcademicQualification, Course, STREAM_CHOICE
from recruiter.models import Job, Recruiter, Application, Shortlist, Placement
from core.decorators import login_required_with_type
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import Announcement
from django.db.models.functions import TruncMonth
from django.db.models import Count
from calendar import month_name
from core.tasks import send_async_mail

@login_required_with_type('admin')
def home(request):
    analytics_job = Job.objects.annotate(month=TruncMonth('posted_date')).values('month').annotate(c=Count('id')).values('month', 'c')
    analytics_placement = Placement.objects.annotate(month=TruncMonth('created_on')).values('month').annotate(c=Count('id')).values('month', 'c')
    dates_job = [f'{d["month"].year} {month_name[d["month"].month]}' for d in analytics_job]
    dates_placment = [f'{d["month"].year} {month_name[d["month"].month]}' for d in analytics_job]
    students_count = Student.objects.all().count()
    recruiters_count = Recruiter.objects.all().count()
    jobs_count = Job.objects.all().count()
    latest_recruiters = reversed(Recruiter.objects.all().order_by('-id')[:5])
    context = {
        'analytics_job': analytics_job, 
        'analytics_placement': analytics_placement, 
        'students_count': students_count,
        'recruiters_count': recruiters_count,
        'jobs_count': jobs_count,
        'latest_recruiters': latest_recruiters,
        'dates': dates_job + dates_placment
    }
    return render(request, 'cgpu_admin/home.html', context)

@login_required_with_type('admin')
def students(request):
    students = Student.objects.all()
    search = request.GET.get('q')
    students = Student.objects.filter(first_name__icontains=search) if search else Student.objects.all() 
    paginator = Paginator(students, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
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
    }
    return render(request, 'cgpu_admin/students.html', context)

@login_required_with_type('admin')
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
    return render(request, 'cgpu_admin/view_student.html', context)

@login_required_with_type('admin')
def deactivate_student_account(request, id):
    student = Student.objects.get(id=id)
    account = student.account
    account.is_active = False 
    account.save()
    return redirect('cgpu_admin:view_student', student.id)

@login_required_with_type('admin')
def activate_student_account(request, id):
    student = Student.objects.get(id=id)
    account = student.account
    account.is_active = True 
    account.save()
    return redirect('cgpu_admin:view_student', student.id)

@login_required_with_type('admin')
def delete_student_account(request, id):
    student = Student.objects.get(id=id)
    student.account.delete()
    student.delete()
    return redirect('cgpu_admin:students')

@login_required_with_type('admin')
def change_student_password(request, id):
    student = Student.objects.get(id=id)
    account = student.account
    account.set_password(request.POST['password'])
    account.save()
    return redirect('cgpu_admin:view_student', student.id)


@login_required_with_type('admin')
def departments(request):
    search = request.GET.get('q')
    departments = Department.objects.filter(name__icontains=search) if search else Department.objects.all() 
    paginator = Paginator(departments, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'departments': current_page.object_list,
        'total_count': departments.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
    }
    return render(request, 'cgpu_admin/departments.html', context)

@login_required_with_type('admin')
def view_department(request, id):
    department = Department.objects.get(id=id)
    courses = Course.objects.filter(department=department)
    students = Student.objects.filter(department=department)
    streams = STREAM_CHOICE
    context = {
        'department': department,
        'courses': courses,
        'students': students,
        'streams': streams,

    }
    return render(request, 'cgpu_admin/view_department.html', context)

@login_required_with_type('admin')
def delete_department(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    return redirect('cgpu_admin:departments')

@login_required_with_type('admin')
def create_course(request, id):
    department = Department.objects.get(id=id)
    Course.objects.create(department=department, course=request.POST['name'], stream=request.POST['stream'])
    return redirect('cgpu_admin:view_department', id)

@login_required_with_type('admin')
def delete_course(request, id, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('cgpu_admin:view_department', id)

@login_required_with_type('admin')
def create_department(request):
    department = Department.objects.create(name=request.POST['name'])
    department.save()
    return redirect('cgpu_admin:departments')

@login_required_with_type('admin')
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
    return render(request, 'cgpu_admin/recruiters.html', context)

@login_required_with_type('admin')
def view_recruiter(request, id):
    recruiter = Recruiter.objects.get(id=id)
    jobs = Job.objects.filter(recruiter=recruiter)

    context = {
        'recruiter': recruiter,
        'jobs': jobs
    }

    return render(request, 'cgpu_admin/view_recruiter.html', context)

@login_required_with_type('admin')
def deactivate_recruiter_account(request, id):
    recruiter = Recruiter.objects.get(id=id)
    account = recruiter.account
    account.is_active = False 
    account.save()
    return redirect('cgpu_admin:view_recruiter', recruiter.id)

@login_required_with_type('admin')
def activate_recruiter_account(request, id):
    recruiter = Recruiter.objects.get(id=id)
    account = recruiter.account
    account.is_active = True 
    account.save()
    return redirect('cgpu_admin:view_recruiter', recruiter.id)

@login_required_with_type('admin')
def delete_recruiter_account(request, id):
    recruiter = Recruiter.objects.get(id=id)
    recruiter.account.delete()
    recruiter.delete()
    return redirect('cgpu_admin:recruiters')

@login_required_with_type('admin')
def change_recruiter_password(request, id):
    recruiter = Recruiter.objects.get(id=id)
    account = recruiter.account
    account.set_password(request.POST['password'])
    account.save()
    return redirect('cgpu_admin:view_recruiter', recruiter.id)


@login_required_with_type('admin')
def jobs(request):
    search = request.GET.get('q')
    jobs = Job.objects.filter(recruiter__name__icontains=search) if search else Job.objects.all() 
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
    return render(request, 'cgpu_admin/jobs.html', context)

@login_required_with_type('admin')
def placements(request):
    search = request.GET.get('q')
    placements = Placement.objects.filter(student__name__icontains=search) if search else Placement.objects.all() 
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
    return render(request, 'cgpu_admin/placements.html', context)

login_required_with_type('admin')
def view_job(request, id):
    job = Job.objects.get(id=id)
    applications = Application.objects.filter(job=job)
    shortlists = Shortlist.objects.filter(job=job)
    context = {
        'job': job,
        'applications': applications,
        'shortlists': shortlists
    }
    return render(request, 'cgpu_admin/view_job.html', context)

@login_required_with_type('admin')
def shortlists(request):
    search = request.GET.get('q')
    shortlists = Shortlist.objects.filter(job__recruiter__name__icontains=search, is_published=True) if search else Shortlist.objects.filter(is_published=True) 
    paginator = Paginator(shortlists, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'shortlists': current_page.object_list,
        'total_count': shortlists.count(),
        'start_index': current_page.start_index(),
        'end_index': current_page.end_index(),
        'has_prev': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'prev': current_page.previous_page_number() if current_page.has_previous() else None,
        'next': current_page.next_page_number() if current_page.has_next() else None,
        'page_range': paginator.page_range,
        'current_page_number': current_page_number,
    }
    return render(request, 'cgpu_admin/shortlists.html', context)

login_required_with_type('admin')
def view_shortlist(request, id):
    shortlist = Shortlist.objects.get(id=id)
    job = Job.objects.get(id=shortlist.job.id)
    applications = Application.objects.filter(job=job)
    shortlisted_applications = shortlist.applications.all()
    applied_applications = [application for application in applications if application not in shortlisted_applications]

    context = {
        'job': job,
        'shortlist': shortlist,
        'shortlisted_applications': shortlisted_applications,
        'applied_applications': applied_applications
    }
    return render(request, 'cgpu_admin/view_shortlist.html', context)


@login_required_with_type('admin')
def announcements(request):
    announcements = Announcement.objects.all()
    context = {
        'announcements': announcements
    }
    return render(request, 'cgpu_admin/announcements.html', context)

@login_required_with_type('admin')
def create_announcement(request):
    announcement = Announcement.objects.create(title=request.POST['title'], description=request.POST['description'])
    student_mail_ids  = [student['email_id'] for student in Student.objects.all().values('email_id')]
    send_async_mail.delay(student_mail_ids, f'New annoucement from cgpu cet: {announcement.title}', announcement.description)
    return redirect('cgpu_admin:announcements')

@login_required_with_type('admin')
def delete_announcement(request, id):
    announcement = Announcement.objects.get(id=id)
    announcement.delete()
    return redirect('cgpu_admin:announcements')

@login_required_with_type('admin')
def accounts(request):
    search = request.GET.get('q')
    accounts = Account.objects.filter(username__icontains=search) if search else Account.objects.all() 
    paginator = Paginator(accounts, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'accounts': current_page.object_list,
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
    return render(request, 'cgpu_admin/accounts.html', context)

@login_required_with_type('admin')
def delete_account(request, id):
    account = Account.objects.get(id=id)
    account.delete()
    return redirect('cgpu_admin:accounts')


@login_required_with_type('admin')
def activate_account(request, id):
    account = Account.objects.get(id=id)
    account.is_active = True
    account.save()
    return redirect('cgpu_admin:accounts')

@login_required_with_type('admin')
def deactivate_account(request, id):
    account = Account.objects.get(id=id)
    account.is_active = False 
    account.save()
    return redirect('cgpu_admin:accounts')

@login_required_with_type('admin')
def create_account(request):
    account = Account(username=request.POST['username'], password=make_password(request.POST['password']), type=request.POST['type'])
    account.save()
    return redirect('cgpu_admin:accounts')

@login_required_with_type('admin')
def bulk_create_student_account(request):
    username_prefix = request.POST['username-prefix']
    password = request.POST['password']
    count = request.POST['count']
    Account.objects.bulk_create(
        [
            Account(
            username=username_prefix+ str(i).zfill(3-len(str(i))),
            password=make_password(password),
            type='student',
            is_active=True,
            ) for i in range(1, int(count)+1)
]
    )
    return redirect('cgpu_admin:accounts')


@login_required_with_type('admin')
def messages(request):
    search = request.GET.get('q')
    accounts = Account.objects.filter(Q(username__icontains=search)&Q(Q(type='recruiter')|Q(type='coordinator'))) if search else Account.objects.filter(Q(type='recruiter')|Q(type='coordinator'))
    paginator = Paginator(accounts, 7)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    for account in current_page.object_list:
        account.new_messages = Message.objects.filter(sender=account, recepient=request.user, read=False).count()
    context = {
        'search': search,
        'accounts': current_page.object_list,
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
    return render(request, 'cgpu_admin/messages.html', context)

@login_required_with_type('admin')
def view_message(request, id):
    account = Account.objects.get(id=id)
    messages = Message.objects.filter(Q(sender=request.user, recepient=account) | Q(recepient=request.user, sender=account)).order_by('created_on')
    messages.filter(recepient=request.user).update(read=True)
    context = {
        'account': account,
        'messages': messages
    }
    return render(request, 'cgpu_admin/view_message.html', context)

@login_required_with_type('admin')
def send_message(request, id):
    account = Account.objects.get(id=id)
    message = Message.objects.create(sender=request.user, recepient=account, content=request.POST['message'])
    send_async_mail.delay([account.email], 'You have a new message from CGPU CET', message.content)
    return redirect('cgpu_admin:view_message', id)

@login_required_with_type('admin')
def delete_message(request, id, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect('cgpu_admin:view_message', id)


