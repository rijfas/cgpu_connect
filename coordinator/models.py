from django.db import models
from core.models import Account

from student.models import Course

# Create your models here.
class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    className = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.className} {self.course.course}"

class Coordinator(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        if (self.middle_name == ""):
            return f"{self.first_name} {self.last_name}"

        return f"{self.first_name} {self.middle_name} {self.last_name}"