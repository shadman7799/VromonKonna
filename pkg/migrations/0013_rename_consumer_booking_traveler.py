# Generated by Django 4.0.6 on 2022-08-19 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pkg', '0012_alter_booking_end_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='traveler',
            new_name='traveler',
        ),
    ]