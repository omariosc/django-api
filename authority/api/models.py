"""
This module contains the models for the database.
These models represent the tables in the provided LaTeX file, 
and their attributes correspond to the table columns. 
Foreign keys are defined using the models.ForeignKey field, 
and unique constraints are specified using the unique=True parameter 
for the respective fields.
"""

from django.db import models


class Airline(models.Model):
    """Stores information about an airline."""

    code = models.CharField(max_length=3, unique=True,
                            primary_key=True, null=False)
    name = models.CharField(max_length=100, unique=True, null=False)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, null=False)
    ip = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.name} ({self.code})'


class Airport(models.Model):
    """Stores information about an airport."""

    ident = models.CharField(
        max_length=100, primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=False)
    iso_country = models.CharField(max_length=100)
    iso_region = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    size_type = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.name} ({self.city}, {self.country})'


class Flight(models.Model):
    """Stores information about a flight."""

    departure_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='departure_flights', null=False)
    destination_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='destination_flights', null=False)
    flight_code = models.CharField(
        max_length=10, unique=True, primary_key=True, null=False)
    departure_datetime = models.DateTimeField(null=False)
    arrival_datetime = models.DateTimeField(null=False)
    duration_time = models.DurationField()
    base_price = models.FloatField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField(null=False)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, null=False)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f'{self.flight_code} [{self.departure_airport} - {self.destination_airport}]'


class Booking(models.Model):
    """Stores information about a booking."""

    booking_ref = models.CharField(
        max_length=10, unique=True, primary_key=True, null=False)
    passport_number = models.IntegerField(null=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.booking_ref} [{self.flight.departure_airport} - {self.flight.destination_airport}]'
