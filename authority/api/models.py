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

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.name} ({self.code})'


class Airport(models.Model):
    """Stores information about an airport."""

    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.name} ({self.city} {self.country})'


class Flight(models.Model):
    """Stores information about a flight."""

    departure_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='departure_flights')
    destination_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='destination_flights')
    flight_code = models.CharField(max_length=10)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    duration_time = models.DurationField()
    base_price = models.FloatField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f'{self.flight_code} ({self.departure_airport} - {self.destination_airport})'


class Booking(models.Model):
    """Stores information about a booking."""

    booking_ref = models.CharField(max_length=10, unique=True)
    passport_number = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return str(self.booking_ref)
