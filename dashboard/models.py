from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=200)
    cameras = models.CharField(max_length=200, blank=True)
    enabled_widgets = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True, upload_to='img/')

    def __str__(self):
        return self.name
