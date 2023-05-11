"""Forms for the authority app."""

from django import forms
from django.core.exceptions import ValidationError
from .models import Flight, Booking


class FlightAdminForm(forms.ModelForm):
    """Form for the Flight model."""

    class Meta:
        """Meta class for the FlightAdminForm class."""

        model = Flight
        fields = '__all__'

    def clean(self):
        """Clean the form data.

        Raises:
            ValidationError: If the flight code already exists.
            ValidationError: If the departure and destination airports are the same.
            ValidationError: If the departure time is after the arrival time.
            ValidationError: If the base price is negative.
            ValidationError: If the total seats is negative.
            ValidationError: If the available seats is negative.
            ValidationError: If the available seats is greater than the total seats.

        Returns:
            dict: The cleaned form data.
        """
        cleaned_data = super().clean()

        flight_code = cleaned_data.get('flight_code')
        departure_airport = cleaned_data.get('departure_airport')
        destination_airport = cleaned_data.get('destination_airport')
        departure_datetime = cleaned_data.get('departure_datetime')
        arrival_datetime = cleaned_data.get('arrival_datetime')
        base_price = cleaned_data.get('base_price')
        total_seats = cleaned_data.get('total_seats')
        available_seats = self.cleaned_data.get('available_seats')

        if Flight.objects.filter(flight_code=flight_code).exists():
            raise ValidationError("This flight already exists.")

        if departure_airport == destination_airport:
            raise ValidationError(
                "Departure and destination airports cannot be the same.")

        if departure_datetime >= arrival_datetime:
            raise ValidationError(
                "Departure time must be before arrival time.")

        if base_price < 0:
            raise ValidationError("Base price cannot be negative.")

        if total_seats < 0:
            raise ValidationError("Total seats cannot be negative.")

        if available_seats < 0:
            raise ValidationError("Available seats cannot be negative.")

        if available_seats > total_seats:
            raise ValidationError(
                "Available seats cannot be greater than total seats.")

        return cleaned_data


class BookingAdminForm(forms.ModelForm):
    """Form for the Booking model."""

    class Meta:
        """Meta class for the BookingAdminForm class."""

        model = Booking
        fields = ['passport_number', 'flight']

    def clean(self):
        """Clean the form data.

        Raises:
            ValidationError: If the passport number is negative.
            ValidationError: If the booking already exists.
            ValidationError: If the flight has no available seats.

        Returns:
            dict: The cleaned form data.
        """
        cleaned_data = super().clean()

        passport_number = cleaned_data.get('passport_number')
        flight = cleaned_data.get('flight')

        # If passport number is negative
        if passport_number and passport_number < 0:
            raise ValidationError("Passport number cannot be negative.")

        # If booking already exists
        if Booking.objects.filter(passport_number=passport_number, flight=flight).exists():
            raise ValidationError("This booking already exists.")

        # If flight has no available seats
        if flight and flight.available_seats == 0:
            raise ValidationError(
                "Cannot create a booking for a flight with no available seats.")

        return cleaned_data
