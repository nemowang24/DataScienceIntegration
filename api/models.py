from django.db import models

# Create your models here.
class Clicks(models.Model):
    counter = models.IntegerField(default=0)
    sessionid = models.CharField(max_length=100)