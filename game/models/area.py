from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=50, unique=True)
