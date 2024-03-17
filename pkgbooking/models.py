from django.db import models
from users.models import *


class Package(models.Model):
    hotel = models.ForeignKey(HotelRep, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    cost = models.IntegerField()
    start_date = models.CharField(max_length=32)
    end_date = models.CharField(max_length=32)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    image = models.ImageField(null=True, blank=True,
                              default='default_pkg.png', upload_to='packages/')

    def __str__(self) -> str:
        return str(self.title)


class PkgImage(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=None)
    image = models.ImageField(null=True, blank=True)
