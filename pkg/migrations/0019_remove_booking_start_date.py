# Generated by Django 4.0.6 on 2022-08-20 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pkg', '0018_booking_start_date_alter_booking_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='start_date',
        ),
    ]
