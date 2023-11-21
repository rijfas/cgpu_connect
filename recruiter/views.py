from django.shortcuts import render
from core.decorators import login_required_with_type


login_required_with_type('recruiter')
def home(request):
    return render(request, 'recruiter/home.html')


login_required_with_type('recruiter')
def profile(request):
    return render(request, 'recruiter/profile.html')

login_required_with_type('recruiter')
def jobs(request):
    return render(request, 'recruiter/jobs.html')


login_required_with_type('recruiter')
def shortlists(request):
    return render(request, 'recruiter/shortlists.html')

login_required_with_type('recruiter')
def messages(request):
    return render(request, 'recruiter/messages.html')
