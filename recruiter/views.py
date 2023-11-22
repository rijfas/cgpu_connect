from django.shortcuts import render, redirect
from .forms import RegisterRecruiterForm
from .models import Recruiter
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
    return render(request, 'recruiter/jobs.html')


login_required_with_type('recruiter')
def shortlists(request):
    return render(request, 'recruiter/shortlists.html')

login_required_with_type('recruiter')
def messages(request):
    return render(request, 'recruiter/messages.html')
