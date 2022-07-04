from django.db import models


class Problem(models.Model):
    question = models.CharField(max_length=300, null=False)
    operation = models.CharField(max_length=20, null=False)
    numbers = models.CharField(max_length=50, null=False)
    result = models.IntegerField(null=False)
    level = models.ForeignKey('game.Level', on_delete= models.CASCADE)