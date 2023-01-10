from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    date_birth = models.DateField(default=timezone.now)
    email = models.EmailField(max_length=50)
    description = models.TextField(max_length=200)
    image = models.ImageField(default='avatar.png', blank=True, null=True)
    phone = models.IntegerField()


    def __str__(self):
        return f"{self.full_name}"

