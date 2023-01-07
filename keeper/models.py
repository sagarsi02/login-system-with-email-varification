from django.db import models

class usr_token(models.Model):
    user = models.IntegerField()
    token = models.CharField(max_length=200)