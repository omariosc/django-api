"""
This module contains the models for the database.
These models represent the tables in the provided LaTeX file, 
and their attributes correspond to the table columns. 
Foreign keys are defined using the models.ForeignKey field, 
and unique constraints are specified using the unique=True parameter 
for the respective fields.
"""

import string
import random
import requests
from django.db import models


class Country(models.Model):
    """Stores information about a country."""

    name = models.CharField(max_length=255, primary_key=True, unique=True)
    continent = models.CharField(max_length=255)
    # any other fields you want to store for a country

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return self.name


class City(models.Model):
    """Stores information about a city."""

    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        """Meta class for the City model."""

        unique_together = ('name', 'country',)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.name}, {self.country.name}'


class Airline(models.Model):
    """Stores information about an airline."""

    code = models.CharField(max_length=3, unique=True,
                            primary_key=True, null=False)
    name = models.CharField(max_length=100, unique=True, null=False)
    ip = models.CharField(max_length=100)

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
    name = models.CharField(max_length=100, unique=True, null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    region = models.CharField(max_length=100)
    size_type = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.CharField(max_length=100)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.name} ({self.city})'


class Flight(models.Model):
    """Stores information about a flight."""

    flight_code = models.CharField(
        max_length=10, unique=True, primary_key=True, null=False)
    departure_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='departure_flights', null=False)
    destination_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='destination_flights', null=False)
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

    def save(self, *args, **kwargs):
        """Overrides the save method to ensure that the number of available seats

        Raises:
            ValueError: If the number of available seats is greater than the total seats.
            ValueError: If the number of available seats is less than zero.
        """

        if self.available_seats < 0:
            raise ValueError('Available seats cannot be less than zero')

        if self.available_seats > self.total_seats:
            raise ValueError(
                'Available seats cannot be greater than total seats')

        super().save(*args, **kwargs)


class Booking(models.Model):
    """Stores information about a booking."""

    booking_ref = models.CharField(
        max_length=10, unique=True, primary_key=True, null=False)
    passport_number = models.IntegerField(null=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=False)

    def __str__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """

        return f'{self.booking_ref} \
            [{self.flight.departure_airport} - {self.flight.destination_airport}]'

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure that the number of available seats
        is updated when a booking is created.
        """

        # If this is a new booking (i.e., it doesn't exist in the database yet)
        if self._state.adding:
            # Generate booking reference
            self.booking_ref = self.generate_booking_ref()

            # Decrease the number of available seats
            self.flight.available_seats -= 1
            self.flight.save()

            # Get the airline IP address
            flight_ip_address = self.flight.airline.ip

            url = f'http://{flight_ip_address}/api/bookings'

            # Make the request data
            data = {
                'booking_ref': self.booking_ref,
                'passport_number': self.passport_number,
                'flight': self.flight.flight_code
            }

            # Make the request
            requests.post(url, data=data, timeout=5)

        super(Booking, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Overrides the delete method to ensure that the number of available seats
        is updated when a booking is deleted.
        """

        # Increase the number of available seats
        self.flight.available_seats += 1
        self.flight.save()

        # Get the airline IP address
        flight_ip_address = self.flight.airline.ip

        url = f'http://{flight_ip_address}/api/bookings/?booking_ref={self.booking_ref}'

        # Make the request data
        data = {
            'booking_ref': self.booking_ref
        }

        # Make the request
        requests.delete(url, data=data, timeout=5)

        super(Booking, self).delete(*args, **kwargs)

    def generate_booking_ref(self):
        """Generates a random booking reference.

        Returns:
            str: The booking reference.
        """
        booking_ref = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        while Booking.objects.filter(booking_ref=booking_ref).exists():
            booking_ref = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))

        return booking_ref
