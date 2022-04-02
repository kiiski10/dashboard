from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='img/')
    camera = models.ForeignKey(
        "Camera",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.name

class Location(models.Model):
    LOCATION_TYPE_CHOICES =(
        ("WAYPOINT", "Waypoint"),
        ("SIGHTS", "Sight seeing"),
        ("CAMP", "Camp site"),
        ("HOME", "Home"),
    )
    creator = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        null=True,
    )
    label = models.CharField(max_length=200)
    note = models.CharField(max_length=200, blank=True)
    location_type = models.CharField(max_length=200, choices=LOCATION_TYPE_CHOICES, default="WAYPOINT")
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return "'{}': {},{}".format(self.label, self.lat, self.lon)


class Camera(models.Model):
    DIRECTION_CHOICES =(
        ("BACK", "Back"),
        ("FORWARD", "Forward"),
        ("LEFT", "Left"),
        ("RIGHT", "Right"),
        ("INTERIOR", "Interior"),
    )
    device_id = models.CharField(max_length=100, default="1")
    label = models.CharField(max_length=200)
    note = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES, default="BACK")

    def __str__(self):
        return "{}: '{}'".format(self.direction, self.label)

