from django.contrib import admin
from .models import Application, Job, Recruiter
# Register your models here.
admin.site.register(Application)
admin.site.register(Job)
admin.site.register(Recruiter)
