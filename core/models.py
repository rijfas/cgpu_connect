from django.db import models
from django.contrib.auth.models import AbstractUser

ACCOUNT_TYPE_CHOICES = (
    ('student', 'Student'),
    ('staff', 'Staff'),
    ('recruiter', 'Recruiter'),
    ('admin', 'Admin'),
)

class Account(AbstractUser):
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='student')

class Message(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender_of_message')
    recepient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reciever_of_message')

    def __str__(self):
        return f'{self.sender}: {self.content}'