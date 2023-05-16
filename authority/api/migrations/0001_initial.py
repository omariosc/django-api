# Generated by Django 4.1.7 on 2023-05-15 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('ident', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('region', models.CharField(max_length=100)),
                ('size_type', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('elevation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('continent', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('departure_datetime', models.DateTimeField()),
                ('arrival_datetime', models.DateTimeField()),
                ('duration_time', models.DurationField()),
                ('base_price', models.FloatField()),
                ('total_seats', models.IntegerField()),
                ('available_seats', models.IntegerField()),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.airline')),
                ('departure_airport',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_flights',
                                   to='api.airport')),
                ('destination_airport',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_flights',
                                   to='api.airport')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.country')),
            ],
            options={
                'unique_together': {('name', 'country')},
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_ref', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('passport_number', models.IntegerField()),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.flight')),
            ],
        ),
        migrations.AddField(
            model_name='airport',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.city'),
        ),
    ]
