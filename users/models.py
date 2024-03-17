from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class HotelRep(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    name = models.CharField(max_length=128)
    address = models.CharField(max_length=512)
    hotline = models.CharField(max_length=11, unique=True)
    catagory = models.CharField(max_length=16)
    image = models.ImageField(null=True, blank=True,
                              default='default_hotel.jpg', upload_to='users/')

    def __str__(self) -> str:
        return str(self.name)


class Traveler(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    name = models.CharField(max_length=128)
    address = models.CharField(max_length=512)
    phone = models.CharField(max_length=11, unique=True)
    emergency_phone = models.CharField(max_length=11, blank=True)
    national_id = models.CharField(max_length=10, unique=True)
    blood_type = models.CharField(max_length=2)
    age = models.SmallIntegerField(2)
    image = models.ImageField(
        null=True, blank=True, default='default_user.jpg', upload_to='users/')

    def __str__(self) -> str:
        return str(self.name)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    time = models.DateTimeField(auto_now_add=True, null=True)
    is_blog = models.BooleanField(default=False)
    is_pkg = models.BooleanField(default=False)

    message = models.CharField(max_length=64, null=True)
    key = models.IntegerField(null=True)

    hidden = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.message)
