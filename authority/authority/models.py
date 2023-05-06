from django.db import models


class Airline(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    code = models.TextField(unique=True)
    name = models.TextField(unique=True)
    country = models.TextField()
    phone = models.TextField(unique=True)


class Airport(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(unique=True)
    city = models.TextField()
    country = models.TextField()


class Flight(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    departure_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departure_flights")
    destination_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_flights")
    departure_date = models.DateField()
    arrival_date = models.DateField()
    duration_time = models.DurationField()
    base_price = models.FloatField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)


class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True, unique=True)
    passport_number = models.IntegerField(unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
