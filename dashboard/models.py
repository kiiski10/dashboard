from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=20)
    image = models.ImageField()
