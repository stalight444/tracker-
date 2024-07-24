from django.db import models

class UserVisit(models.Model):
    device_info = models.TextField()
    geolocation = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
