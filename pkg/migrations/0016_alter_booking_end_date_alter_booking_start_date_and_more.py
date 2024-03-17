# Generated by Django 4.0.6 on 2022-08-20 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pkg', '0015_booking_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='package',
            name='start_date',
            field=models.DateField(),
        ),
    ]
