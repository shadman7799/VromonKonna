from django.db import models
from users.models import *


class Package(models.Model):
    author = models.ForeignKey(HotelRep, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    cost = models.IntegerField()

    start_date = models.DateField()
    end_date = models.DateField()

    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    rating = models.FloatField(null=True, default=0.0)
    total = models.IntegerField(null=True, default=0)

    image = models.ImageField(null=True, blank=True,
                              default='default_pkg.png', upload_to='packages/')

    def __str__(self) -> str:
        return "Name: " + str(self.title) + "\tDestination: " + str(self.destination)


class Booking(models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    email = models.CharField(max_length=32)

    start_date = models.DateField(null=True)
    end_date = models.DateField()

    def __str__(self) -> str:
        return str(self.traveler.name) + "  booked  " + str(self.package.title)


class Review(models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    # title = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    rating = models.IntegerField()

    def __str__(self) -> str:
        return str(self.traveler.name) + "  rated  " + str(self.package.destination)


class PkgImage(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=None)
    image = models.ImageField(null=True, blank=True, upload_to='packages/')
