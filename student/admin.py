from django.contrib import admin
from .models import Student, AcademicQualification, Course, Department, Result
# Register your models here.
admin.site.register(Student)
admin.site.register(AcademicQualification)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Result)
