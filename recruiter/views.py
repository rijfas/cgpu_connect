from django.shortcuts import render, redirect
from .forms import RegisterRecruiterForm, AddJobForm
from .models import Recruiter, Job, Application, Shortlist, SHORTLIST_TYPE_CHOICES, Placement
from core.models import Account, Message
from student.models import Course
from core.decorators import login_required_with_type
from django.db.models import Q
from django.core.paginator import Paginator
from core.tasks import send_async_mail
from student.models import Student

login_required_with_type('recruiter')
def register(request):
    if request.method == 'POST':
        request.user.email = request.POST['email_id']
        request.user.save()
        form = RegisterRecruiterForm(request.POST)
        recruiter = form.save(commit=False)
        recruiter.account = request.user 
        if form.is_valid():
            form.save()
            return redirect('recruiter:home')
    form = RegisterRecruiterForm()
    context = {
        'form': form
    }
    return render(request, 'recruiter/register.html', context)

login_required_with_type('recruiter')
def home(request):
    recruiter = Recruiter.objects.get(account=request.user)
    recent_applications = Application.objects.filter(job__recruiter=recruiter).order_by('-id')[:5]
    recent_messages = Message.objects.filter(recepient=request.user).order_by('-id')[:5]
    number_of_applications = Application.objects.filter(job__recruiter=recruiter).count()
    number_of_jobs = Job.objects.filter(recruiter=recruiter).count()
    context = {
        'recent_applications': recent_applications,
        'recent_messages': recent_messages,
        'number_of_applications': number_of_applications,
        'number_of_jobs': number_of_jobs
    }
    return render(request, 'recruiter/home.html', context)


login_required_with_type('recruiter')
def profile(request):
    profile = Recruiter.objects.get(account=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'recruiter/profile.html', context)

login_required_with_type('recruiter')
def jobs(request):
    profile = Recruiter.objects.get(account=request.user)
    courses = Course.objects.all()
    form = AddJobForm()
    search = request.GET.get('q')
    jobs = Job.objects.filter(Q(role__icontains=search)&Q(recruiter=profile)) if search else Job.objects.filter(recruiter=profile) 
    paginator = Paginator(jobs, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'form': form,
        'courses': courses,
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
    return render(request, 'recruiter/jobs.html', context)

login_required_with_type('recruiter')
def applications(request):
    profile = Recruiter.objects.get(account=request.user)
    search = request.GET.get('q')
    applications = Application.objects.filter(Q(job__recruiter=profile) & Q(student__first_name__icontains=search)) if search else Application.objects.filter(job__recruiter=profile) 
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
    return render(request, 'recruiter/applications.html', context)

login_required_with_type('recruiter')
def view_application(request, id):
    application = Application.objects.get(id=id)
    context = {
        'application': application
    }
    return render(request, 'recruiter/view_application.html', context)

login_required_with_type('recruiter')
def view_job(request, id):
    job = Job.objects.get(id=id)
    shortlist = Shortlist.objects.filter(job=job)
    job.is_shortlist_created = len(shortlist) != 0
    applications = Application.objects.filter(job=job)
    shortlists = Shortlist.objects.filter(job=job)
    context = {
        'job': job,
        'applications': applications,
        'shortlists': shortlists,
        'shortlist_types': SHORTLIST_TYPE_CHOICES,

    }
    return render(request, 'recruiter/view_job.html', context)

login_required_with_type('recruiter')
def create_job(request):
    profile = Recruiter.objects.get(account=request.user)
    job = Job(
        recruiter = profile,
        role = request.POST['role'],
        description = request.POST['description'],
        job_type = request.POST['job_type'],
        slab = '1' if int(request.POST['ctc']) <= 6 else '2' if int(request.POST['ctc']) <= 12 else '3',
        ctc = request.POST['ctc'],
        can_placed_students_apply = True if request.POST.get('can_placed_students_apply') else False,
        application_deadline = request.POST['application_deadline'],
        maximum_backlogs = None if request.POST['maximum_backlogs'] == '' else request.POST['maximum_backlogs'],
        maximum_active_backlogs = None if request.POST['maximum_active_backlogs'] == '' else request.POST['maximum_active_backlogs'],
        min_gpa = None if request.POST['min_gpa'] == '' else request.POST['min_gpa'],
    )
    eligible_courses_id = [int(value) for key,value in request.POST.items() if key.startswith('eligible_course')]
    job.save()
    eligible_courses = Course.objects.filter(id__in=eligible_courses_id)
    job.eligible_courses.add(*eligible_courses_id)
    job.save()
    student_emails = [student['email_id'] for student in Student.objects.filter(course__in=eligible_courses).values('email_id')]
    send_async_mail.delay(student_emails, f"CGPU Connect: Recruitement by {profile.name} for {job.role}", f"Recruitement by {profile.name} for {job.role} check cgpu connect for more info")
    return redirect('recruiter:jobs')

login_required_with_type('recruiter')
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
    return render(request, 'recruiter/view_shortlist.html', context)

login_required_with_type('recruiter')
def add_to_shortlist(request, id, application_id):
    shortlist = Shortlist.objects.get(id=id)
    application = Application.objects.get(id=application_id)
    shortlist.applications.add(application)
    return redirect('recruiter:view_shortlist', id)

login_required_with_type('recruiter')
def add_all_to_shortlist(request, id):
    shortlist = Shortlist.objects.get(id=id)
    job = Job.objects.get(id=shortlist.job.id)
    applications = Application.objects.filter(job=job)
    shortlisted_applications = shortlist.applications.all()
    applied_applications = [application for application in applications if application not in shortlisted_applications]
    shortlist.applications.add(*applied_applications)
    return redirect('recruiter:view_shortlist', id)

login_required_with_type('recruiter')
def remove_from_shortlist(request, id, application_id):
    application = Application.objects.get(id=application_id)
    shortlist = Shortlist.objects.get(job=application.job)
    shortlist.applications.remove(application)
    return redirect('recruiter:view_shortlist', id)

login_required_with_type('recruiter')
def remove_all_from_shortlist(request, id):
    shortlist = Shortlist.objects.get(id=id)
    shortlist.applications.remove(*shortlist.applications.all())
    return redirect('recruiter:view_shortlist', id)

login_required_with_type('recruiter')
def publish_shortlist(request, id):
    shortlist = Shortlist.objects.get(id=id)
    shortlist.is_published = True 
    shortlist.save()
    shortlisted_applications = shortlist.applications.all()
    for application in shortlisted_applications:
        application.status = shortlist.type 
        application.save()
    if shortlist.type == 'CLR':
        for application in shortlisted_applications:
            Placement.objects.create(job=application.job, student=application.student)
    shortlisted_student_mail_ids = [application.student.email_id for application in shortlisted_applications]
    send_async_mail.delay(shortlisted_student_mail_ids, f"CGPU Connect: Shortlisted update for {shortlist.job}", f"Your application of {shortlist.job} is shortlisted for {shortlist.get_type_display()} check cgpu connect dashboard for more info")
    return redirect('recruiter:view_shortlist', id)

login_required_with_type('recruiter')
def shortlists(request):
    recruiter = Recruiter.objects.get(account=request.user)
    jobs = Job.objects.filter(recruiter=recruiter)
    search = request.GET.get('q')
    shortlists = Shortlist.objects.filter(Q(job__recruiter=recruiter) & Q(job__role__icontains=search)) if search else Shortlist.objects.filter(job__recruiter=recruiter) 
    paginator = Paginator(shortlists, 11)
    current_page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(current_page_number)
    context = {
        'search': search,
        'jobs': jobs,
        'shortlist_types': SHORTLIST_TYPE_CHOICES,
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
    return render(request, 'recruiter/shortlists.html', context)


login_required_with_type('recruiter')
def delete_shortlist(request, id):
    shortlist = Shortlist.objects.get(id=id)
    shortlist.delete() 
    return redirect('recruiter:shortlists')

login_required_with_type('recruiter')
def create_shortlist(request):
    recruiter = Recruiter.objects.get(account=request.user)
    job = Job.objects.get(id=int(request.POST['job']))
    Shortlist.objects.create(recruiter=recruiter,job=job, type=request.POST['type']) 
    return redirect('recruiter:shortlists')

login_required_with_type('recruiter')
def messages(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(recepient=request.user)).order_by('created_on')
    messages.filter(recepient=request.user).update(read=True)
    context = {
        'messages': messages
    }
    return render(request, 'recruiter/messages.html', context)


@login_required_with_type('recruiter')
def send_message(request):
    account = Account.objects.get(type='admin')
    message = Message.objects.create(sender=request.user, recepient=account, content=request.POST['message'])
    send_async_mail.delay([account.email], f'CGPU Connect: You have a new message from {request.user}', message.content)


    return redirect('recruiter:messages')

@login_required_with_type('recruiter')
def delete_message(request, id):
    message = Message.objects.get(id=id)
    message.delete()
    return redirect('recruiter:messages')
