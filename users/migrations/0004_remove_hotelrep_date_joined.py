# Generated by Django 4.0.6 on 2022-07-22 18:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_remove_hotelrep_two_factor_auth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelrep',
            name='date_joined',
        ),
    ]
