"""This module contains the viewsets for the Flight and Booking endpoints."""

from rest_framework.views import APIView
from datetime import date
from django.db.models import Sum, Q, F, ExpressionWrapper, FloatField
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer


class FlightViewSet(viewsets.GenericViewSet):
    """Viewset for the Flight model."""

    queryset = Flight.objects.none()
    serializer_class = FlightSerializer

    @action(detail=False, methods=['get'], serializer_class=FlightSerializer)
    def get_flights(self, request):
        """Returns a list of all flights, or a specific flight if a flight_code is provided.

        Returns:
            Response: List of all flights, or a specific flight.
        """
        flight_code = request.query_params.get('flight_code', None)

        if flight_code:
            # Get the specific flight with the provided flight_code
            flights = Flight.objects.filter(flight_code=flight_code)
            if not flights.exists():
                return Response({"detail": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get all flights
            flights = Flight.objects.all()
            if not flights.exists():
                return Response({"detail": "No flights available."}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(flights, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], serializer_class=FlightSerializer)
    def create_flight(self, request):
        """Creates a new flight.

        Args:
            request (Request): The flight details.

        Returns:
            Response: The response object.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], serializer_class=FlightSerializer)
    def delete_flight(self, request):
        """Deletes a flight.

        Args:
            request (Request): The flight code.

        Returns:
            Response: The response object.
        """
        flight_code = request.data.get('flight_code')
        if not flight_code:
            return Response(
                {"error": "Flight code is required"},
                status=status.HTTP_400_BAD_REQUEST)

        flight = Flight.objects.filter(flight_code=flight_code).first()
        if not flight:
            return Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)

        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingViewSet(viewsets.GenericViewSet):
    """Viewset for the Booking model."""

    serializer_class = BookingSerializer

    @action(detail=False, methods=['post'], serializer_class=BookingSerializer)
    def create_booking(self, request):
        """Creates a new booking.

        Args:
            request (Request): The booking details.

        Returns:
            Response: The response object.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], serializer_class=BookingSerializer)
    def delete_booking(self, request):
        """Deletes a booking.

        Args:
            request (Request): The booking reference.

        Returns:
            Response: The response object.
        """

        booking_ref = request.data.get('booking_ref')
        if not booking_ref:
            return Response(
                {"error": "Booking reference is required"},
                status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.filter(booking_ref=booking_ref).first()
        if not booking:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PassengersPerAirlineToday(APIView):
    """Returns the number of passengers per airline for today."""

    def get(self, request, format=None):
        today = date.today()
        # Use bookings to get the number of passengers per airline
        data = Booking.objects.filter(
            flight__airline__isnull=False,
            flight__departure_datetime__date=today
        ).values('flight__airline__name').annotate(
            passengers=Sum('flight_id')
        ).order_by('-passengers')

        return Response(data)


class FlightIncomeData(APIView):
    """Returns the income per airline, departure airport, and flight."""

    def get(self, request, format=None):
        data = Flight.objects.annotate(
            income=ExpressionWrapper(
                (F('total_seats') - F('available_seats')) * F('base_price'),
                output_field=FloatField()
            )
        ).values(
            'airline__name',
            'departure_airport__name',
            'departure_airport__city',
            'departure_airport__country', 'income')

        return Response(data)
