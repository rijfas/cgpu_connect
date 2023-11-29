from django.db import models
from core.models import Account

from student.models import Class

# Create your models here.
class Coordinator(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.CharField(max_length=30, blank=False, null=False)
    section = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"