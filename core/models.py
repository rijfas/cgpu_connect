from django.db import models
from django.contrib.auth.models import AbstractUser

ACCOUNT_TYPE_CHOICES = (
    ('student', 'Student'),
    ('staff', 'Staff'),
    ('recruiter', 'Recruiter'),
    ('coordinator', 'Coordinator'),
    ('admin', 'Admin'),
)

class Account(AbstractUser):
    type = models.CharField(max_length=15, choices=ACCOUNT_TYPE_CHOICES, default='student')

