# Generated by Django 4.2.1 on 2023-05-13 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotelapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('is_available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, upload_to='photos/')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Room_booked', to='hotelapp.room')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Booked_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
