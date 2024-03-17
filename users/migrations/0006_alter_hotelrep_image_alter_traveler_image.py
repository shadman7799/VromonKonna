# Generated by Django 4.0.6 on 2022-08-13 05:33

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_hotelrep_image_alter_traveler_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelrep',
            name='image',
            field=models.ImageField(blank=True, default='default_hotel.jpg', null=True, upload_to=pathlib.PureWindowsPath('G:/Development/CSE347 Project/Vromonkonna/static/images')),
        ),
        migrations.AlterField(
            model_name='traveler',
            name='image',
            field=models.ImageField(blank=True, default='default_user.jpg', null=True, upload_to=pathlib.PureWindowsPath('G:/Development/CSE347 Project/Vromonkonna/static/images')),
        ),
    ]
