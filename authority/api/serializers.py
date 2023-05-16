"""This module contains the serializers for the authority app."""

from rest_framework import serializers

from .models import Airline, Airport, Flight, Booking, City, Country


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
        fields = ('booking_ref', 'flight', 'passport_number')
        read_only_fields = ('booking_ref',)

    def create(self, validated_data):
        """Create a new booking.

        Args:
            validated_data (dict): The validated data.

        Returns:
            Booking: The created booking.
        """

        validated_data['booking_ref'] = Booking.generate_booking_ref()
        return super().create(validated_data)


class AirlineSerializer(serializers.ModelSerializer):
    """Serializes the Airline model."""

    class Meta:
        """Meta class for the AirlineSerializer."""

        model = Airline
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):
    """Serializes the Airport model."""

    class Meta:
        """Meta class for the AirportSerializer."""

        model = Airport
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    """Serializes the City model."""

    class Meta:
        """Meta class for the CitySerializer."""

        model = City
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    """Serializes the Country model."""

    class Meta:
        """Meta class for the CountrySerializer."""

        model = Country
        fields = '__all__'
