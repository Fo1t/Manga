from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    AVAILABILITY_MODE = [
        ('l', 'Light'),
        ('d', 'Dark'),
    ]
    mode = models.CharField(max_length=1, choices=AVAILABILITY_MODE, default='l', null=False)