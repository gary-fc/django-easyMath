from django.db import models




class Level(models.Model):
    name = models.CharField(max_length=50, unique=False)
    area = models.ForeignKey('game.Area', models.CASCADE)