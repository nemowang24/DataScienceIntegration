from django.db import models

# Create your models here.
class Clicks(models.Model):
    counter = models.IntegerField(default=0)
    sessionid = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class Prompts(models.Model):
    model = models.CharField(max_length=100)
    resolution = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    note = models.CharField(max_length=1000)
    prompt = models.CharField(max_length=5000)
    img_path = models.CharField(max_length=500)
    sessionid = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)