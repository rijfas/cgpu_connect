from django.shortcuts import render, redirect
from core.models import Account
from django.core.exceptions import ObjectDoesNotExist
from student.models import Student, Department, AcademicQualification
from recruiter.models import Job, Recruiter
from core.decorators import login_required_with_type
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password

@login_required_with_type('admin')
def home(request):
    students_count = Student.objects.all().count()
    recruiters_count = Recruiter.objects.all().count()
    jobs_count = Job.objects.all().count()
    latest_recruiters = reversed(Recruiter.objects.all().order_by('-id')[:5])
    context = {
        'students_count': students_count,
        'recruiters_count': recruiters_count,
        'jobs_count': jobs_count,
        'latest_recruiters': latest_recruiters,
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
def create_department(request):
    department = Department.objects.create(name=request.POST['name'])
    department.save()
    return redirect('cgpu_admin:departments')

@login_required_with_type('admin')
def recruiters(request):
    recruiters = Recruiter.objects.all()
    context = {
        'recruiters': recruiters
    }
    return render(request, 'cgpu_admin/recruiters.html', context)

@login_required_with_type('admin')
def jobs(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
    return render(request, 'cgpu_admin/jobs.html', context)

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


