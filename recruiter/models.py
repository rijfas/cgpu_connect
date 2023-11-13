from django.db import models
from core.models import Account

from student.models import Student, Department

JOB_TYPE_CHOICES = (
    ('Internship', 'Internship'),
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
)

APPLICATION_STATUS_CHOICES = (
    ('APL', 'Applied'),
    ('VRF', 'Verified'),
    ('REJ', 'Rejected'),
    ('HOL', 'On Hold'),
    ('TSP', 'Test Passed'),
    ('TSF', 'Test Failed'),
    ('SHR', 'Shortlisted For Interview'),
    ('NSH', 'Not Shortlisted'),
    ('CLR', 'Cleared the process'),
)

SLAB_CHOICES = (
    ('1', 'First'),
    ('2', 'Second'),
    ('3', 'Third'),
    ('D', 'Dream'),
)

class Recruiter(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.CharField(max_length=30, blank=False, null=False)
    website = models.CharField(max_length=50)

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    description = models.TextField()
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES)
    slab = models.CharField(max_length=10, choices=SLAB_CHOICES)
    ctc = models.DecimalField(max_digits=5, decimal_places=2)
    can_placed_students_apply = models.BooleanField()
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    maximum_backlogs = models.IntegerField(default=0)
    maximum_active_backlogs = models.IntegerField(default=0)
    min_gpa = models.FloatField()
    eligible_departments = models.ManyToManyField(Department)

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=APPLICATION_STATUS_CHOICES, default='APL')
    remarks = models.CharField(max_length=150, null=True, blank=True)
