from django.contrib import admin
from .models import Application, Job, Recruiter, Shortlist
# Register your models here.
admin.site.register(Application)
admin.site.register(Job)
admin.site.register(Recruiter)
admin.site.register(Shortlist)
