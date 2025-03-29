from django.conf import settings
from django.db import models



class AccessStatistic(models.Model):
    user = models.CharField(max_length=30, default='Unknown')
    access_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=30, default='Unknown')
    url_visited = models.CharField(max_length=200, default='Unknown ')
    browser_info =models.CharField(max_length=200, default='Unknown ')
    is_robot = models.BooleanField(default=False)
    owner = models.CharField(max_length=200, default='Unknown')
    detail_ipinfo = models.CharField(max_length=2048, default='Unknown')

    def __str__(self):
        return f"{self.user} accessed on {self.access_time}"
