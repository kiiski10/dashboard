from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=20, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car"

