from django.shortcuts import render, redirect
from .forms import RegisterRecruiterForm, AddJobForm
from .models import Recruiter, Job, Application, Shortlist
from core.models import Account, Message
from student.models import Course
from core.decorators import login_required_with_type
from django.db.models import Q


login_required_with_type('recruiter')
def register(request):
    if request.method == 'POST':
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
    jobs = Job.objects.filter(recruiter=profile)
    courses = Course.objects.all()
    form = AddJobForm()
    context = {
        'jobs': jobs,
        'form': form,
        'courses': courses,
    }
    return render(request, 'recruiter/jobs.html', context)

login_required_with_type('recruiter')
def applications(request):
    profile = Recruiter.objects.get(account=request.user)
    applications = Application.objects.filter(job__recruiter=profile)
    context = {
        'applications': applications
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
    context = {
        'job': job,
        'applications': applications
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
    job.eligible_courses.add(*Course.objects.filter(id__in=eligible_courses_id))
    job.save()
    return redirect('recruiter:jobs')

login_required_with_type('recruiter')
def view_shortlist(request, id):
    job = Job.objects.get(id=id)
    applications = Application.objects.filter(job=job)
    shortlist, _ = Shortlist.objects.get_or_create(job=job)
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
def add_to_shortlist(request, id):
    application = Application.objects.get(id=id)
    shortlist = Shortlist.objects.get(job=application.job)
    shortlist.applications.add(application)
    return redirect('recruiter:view_shortlist', application.job.id)

login_required_with_type('recruiter')
def remove_from_shortlist(request, id):
    application = Application.objects.get(id=id)
    shortlist = Shortlist.objects.get(job=application.job)
    shortlist.applications.remove(application)
    return redirect('recruiter:view_shortlist', application.job.id)

login_required_with_type('recruiter')
def publish_shortlist(request, id):
    shortlist = Shortlist.objects.get(job=id)
    shortlist.is_published = True 
    shortlist.save()
    return redirect('recruiter:view_shortlist', id)

login_required_with_type('recruiter')
def shortlists(request):
    recruiter = Recruiter.objects.get(account=request.user)
    shortlists = Shortlist.objects.filter(job__recruiter=recruiter)
    context = {
        'shortlists': shortlists
    }
    return render(request, 'recruiter/shortlists.html', context)

login_required_with_type('recruiter')
def messages(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(recepient=request.user)).order_by('created_on')
    context = {
        'messages': messages
    }
    return render(request, 'recruiter/messages.html', context)


@login_required_with_type('recruiter')
def send_message(request):
    account = Account.objects.get(type='admin')
    Message.objects.create(sender=request.user, recepient=account, content=request.POST['message'])

    return redirect('recruiter:messages')

@login_required_with_type('recruiter')
def delete_message(request, id):
    message = Message.objects.get(id=id)
    message.delete()
    return redirect('recruiter:messages')
