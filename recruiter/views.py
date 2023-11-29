from django.shortcuts import render, redirect
from .forms import RegisterRecruiterForm, AddJobForm
from .models import Recruiter, Job
from student.models import Course
from core.decorators import login_required_with_type

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
    return render(request, 'recruiter/home.html')


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
def shortlists(request):
    return render(request, 'recruiter/shortlists.html')

login_required_with_type('recruiter')
def messages(request):
    return render(request, 'recruiter/messages.html')
