from django.db import models
from core.models import Account

from student.models import Student, Course

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

SHORTLIST_TYPE_CHOICES = (
    ('VRF', 'Verified'),
    ('TSP', 'Test Passed'),
    ('SHR', 'Shortlisted For Interview'),
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

    def __str__(self):
        return self.name

class Application(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=APPLICATION_STATUS_CHOICES, default='APL')
    remarks = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f'for {self.job} by {self.student}'
    
class Shortlist(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=SHORTLIST_TYPE_CHOICES, default='VRF')
    applications = models.ManyToManyField(Application)
    is_published = models.BooleanField(default=False)

    def students(self):
        return [application.student for application in self.applications.all()]


class Job(models.Model):
    is_open = models.BooleanField(default=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    description = models.TextField()
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES)
    slab = models.CharField(max_length=10, choices=SLAB_CHOICES)
    ctc = models.DecimalField(max_digits=5, decimal_places=2)
    can_placed_students_apply = models.BooleanField()
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    maximum_backlogs = models.IntegerField(null=True, blank=True)
    maximum_active_backlogs = models.IntegerField(null=True, blank=True)
    min_gpa = models.FloatField(null=True, blank=True)
    eligible_courses = models.ManyToManyField(Course)

    def number_of_applicants(self):
        return Application.objects.filter(job=self).count()
    
    def applicants(self):
        return Application.objects.filter(job=self)
    
    def __str__(self):
        return f'{self.role} at {self.recruiter}'


