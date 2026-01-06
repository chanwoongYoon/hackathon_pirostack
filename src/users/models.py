from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    role = models.CharField(max_length=10, default="empty_role")
    name = models.CharField(max_length=10, default="empty_name")
    phone_number = models.CharField(max_length=10, default="010-0000-0000")
    password = models.CharField(max_length=20, default="empty_code")
    permission = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
