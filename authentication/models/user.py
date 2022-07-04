from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    school = models.CharField(max_length=250, unique=False)
    score = models.IntegerField(default=0,null=True)
    total_score = models.IntegerField(default=0, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

