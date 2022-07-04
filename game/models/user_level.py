from django.db import models


class UserLevel(models.Model):
    name_user_level = models.CharField(max_length=50, unique=False)