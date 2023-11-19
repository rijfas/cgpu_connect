from django.shortcuts import render, redirect
from core.models import Account
from student.models import Department
from core.decorators import login_required_with_type
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

@login_required_with_type('admin')
def home(request):
    return render(request, 'cgpu_admin/home.html')

@login_required_with_type('admin')
def students(request):
    return render(request, 'cgpu_admin/students.html')

@login_required_with_type('admin')
def departments(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'cgpu_admin/departments.html', context)

@login_required_with_type('admin')
def recruiters(request):
    return render(request, 'cgpu_admin/recruiters.html')

@login_required_with_type('admin')
def jobs(request):
    return render(request, 'cgpu_admin/jobs.html')

@login_required_with_type('admin')
def shortlists(request):
    return render(request, 'cgpu_admin/shortlists.html')

@login_required_with_type('admin')
def learning(request):
    return render(request, 'cgpu_admin/learning.html')

@login_required_with_type('admin')
def announcements(request):
    return render(request, 'cgpu_admin/announcements.html')

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
            is_active=True,
            ) for i in range(1, int(count)+1)
]
    )
    return redirect('cgpu_admin:accounts')


