from django.contrib.auth.decorators import user_passes_test


def admin_login_required(function):
    actual_decorator = user_passes_test(lambda u: u.type=='admin')
    return actual_decorator(function)

def staff_login_required(function):
    actual_decorator = user_passes_test(lambda u: u.type=='staff')
    return actual_decorator(function)

def student_login_required(function):
    actual_decorator = user_passes_test(lambda u: u.type=='student')
    return actual_decorator(function)

def recruiter_login_required(function):
    actual_decorator = user_passes_test(lambda u: u.type=='recruiter')
    return actual_decorator(function)