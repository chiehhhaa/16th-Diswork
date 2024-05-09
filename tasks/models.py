from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    situation=models.ForeignKey(
        'Situation',
        on_delete=models.CASCADE
    )
    created_user_name=models.CharField(max_length=20)
    title=models.CharField(max_length=20)
    content=models.TextField(default='')
    created_at=models.DateTimeField(auto_now_add=True)
    start_time=models.DateTimeField(null=True)
    end_time=models.DateTimeField(null=True)

class TakeTask(models.Model):
    task=models.ForeignKey(
        'Task',
        on_delete=models.CASCADE
    )

class Situation(models.Model):
    name=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

