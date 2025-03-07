from django.db import models

# Create your models here.
class Userbase(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    birthday = models.DateField()
    active = models.BooleanField(default=False)