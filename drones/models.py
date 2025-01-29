from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class DroneCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Drone(models.Model):
    name = models.CharField(max_length=120, unique=True)
    drone_category = models.ForeignKey(
        DroneCategory, on_delete=models.CASCADE, related_name="drones"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="drones",
        default=1,
    )
    manufacturing_date = models.DateTimeField()
    is_participant = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.name


class Pilot(models.Model):
    MALE = "M"
    FEMALE = "F"
    genders = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    name = models.CharField(max_length=120, unique=True)
    gender = models.CharField(max_length=2, choices=genders, default=MALE)
    races_amount = models.IntegerField(default=0)
    pilot_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    pilot = models.ForeignKey(
        Pilot, on_delete=models.CASCADE, related_name="competitions"
    )
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    distance_in_meters = models.IntegerField()
    achieved_distance_date = models.DateTimeField()

    class Meta:
        ordering = ("-distance_in_meters",)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
