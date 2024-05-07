from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    name = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True, default="")
    vip_user = models.CharField(max_length=50, default="")
    vip_date_expiry = models.DateTimeField(null=True, blank=True)
