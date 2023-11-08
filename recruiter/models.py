from django.db import models
from django.contrib.auth.models import User

#Imports from foreign apps
from student.models import StudentProfile

JOB_TYPE_CHOICES = (
    ('Internship', 'Internship'),
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
)

SHORTLIST_PROCESS_CHOICES = (
    ('TEST', 'Test'),
    ('TECH INT', 'Technical Interview'),
    ('HR INT', 'HR Interview'),
    ('PLCD', 'Placed')
)

class RecruiterData(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.CharField(max_length=30, blank=False, null=False)
    url = models.CharField(max_length=50)

class Job(models.Model):
    recruiter = models.ForeignKey(RecruiterData, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    #The following fields may or may not be required as the Job Description can cover them
    posted_date = models.DateTimeField()
    deadline = models.DateTimeField()
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES)
    backlog_constraint = models.BooleanField(default=False)
    active_backlog_constraint = models.BooleanField(default=False)
    min_gpa = models.FloatField()
    #eligible_courses

class Shortlist(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    process = models.CharField(max_length=30, choices=SHORTLIST_PROCESS_CHOICES)
    students = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='students_shortlist')