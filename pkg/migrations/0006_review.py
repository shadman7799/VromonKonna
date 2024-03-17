# Generated by Django 4.0.6 on 2022-08-17 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_hotelrep_image_alter_traveler_image'),
        ('pkg', '0005_remove_booking_total_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale', models.IntegerField()),
                ('traveler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.traveler')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pkg.package')),
            ],
        ),
    ]
