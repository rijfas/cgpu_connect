from django.db import models

# Create your models here.
class Announcement(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title