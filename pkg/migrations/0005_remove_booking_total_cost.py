# Generated by Django 4.0.6 on 2022-08-17 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pkg', '0004_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='total_cost',
        ),
    ]
