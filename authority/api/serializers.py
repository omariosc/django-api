"""This module contains the serializers for the authority app."""

from rest_framework import serializers
from .models import Airline, Airport, Flight, Booking


class FlightSerializer(serializers.ModelSerializer):
    """Serializes the Flight model."""

    class Meta:
        """Meta class for the FlightSerializer."""

        model = Flight
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """Serializes the Booking model."""

    class Meta:
        """Meta class for the BookingSerializer."""

        model = Booking
        fields = '__all__'


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'
