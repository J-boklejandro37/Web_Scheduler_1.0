from django.db import models

# Create your models here.
class Userbase(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    birthday = models.DateField()
    active = models.BooleanField(default=False)

class Tasks(models.Model):
    user_id = models.IntegerField()
    date = models.DateField()
    task_title = models.CharField(max_length=30)
    task_content = models.TextField()
    task_time = models.CharField(max_length=1)

class DailyCheckbox(models.Model):
    user_id = models.IntegerField()
    task = models.CharField(max_length=30)
    checked = models.BooleanField(default=False)