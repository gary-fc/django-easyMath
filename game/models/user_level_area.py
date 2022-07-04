from django.db import models




class UserLevelArea(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    level = models.ForeignKey('game.Level', on_delete=models.CASCADE)
    area = models.ForeignKey('game.Area', on_delete=models.CASCADE)
    finalized = models.BooleanField(default=False, null=False)
    maximum_points_obtained = models.IntegerField(default=0, null=False)
    minimum_points_obtained = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)