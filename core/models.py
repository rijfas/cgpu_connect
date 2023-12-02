from django.db import models
from django.contrib.auth.models import AbstractUser

ACCOUNT_TYPE_CHOICES = (
    ('student', 'Student'),
    ('staff', 'Staff'),
    ('recruiter', 'Recruiter'),
    ('coordinator', 'Coordinator'),
    ('admin', 'Admin'),
)




class Message(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    sender = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='sender_of_message')
    recepient = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='reciever_of_message')
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}: {self.content}'

class Account(AbstractUser):
    type = models.CharField(max_length=15, choices=ACCOUNT_TYPE_CHOICES, default='student')

    def has_unread_messages(self):
        return Message.objects.filter(recepient=self, read=False).exists()