from django.db import models

# Create your models here.
class Clicks(models.Model):
    counter = models.IntegerField(default=0)
    sessionid = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class Prompts(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=20)
    resolution = models.CharField(max_length=20)
    quality = models.CharField(max_length=20)
    note = models.CharField(max_length=1000)
    prompt = models.CharField(max_length=1000)
    img_path = models.CharField(max_length=200)
    sessionid = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    processed = models.IntegerField(default=0)
    imgen_result = models.CharField(max_length=3000, default="")
    time_used = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)
