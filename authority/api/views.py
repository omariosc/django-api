"""This module contains the viewsets for the Flight and Booking endpoints."""

import requests
from django.views.static import serve
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import AirportFilter, FlightFilter
from .models import Airline, Airport, Flight, Booking, City, Country
from .serializers import AirlineSerializer, AirportSerializer, \
    FlightSerializer, BookingSerializer, CitySerializer, CountrySerializer


def get_param(param, request):
    """Gets a parameter from the request.

    Args:
        param (str): The parameter to get.
        request (Request): The request object.

    Returns:
        str: The parameter value.
    """

    query = request.query_params.get(param)
    return query if query else request.data.get(param)


class AirlineViewSet(viewsets.GenericViewSet):
    """This class defines the viewset for the Airline endpoint."""

    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['get'], serializer_class=AirlineSerializer)
    def get_airlines(self, request):
        """
        Returns a list of all airlines.
        If the airline_code parameter is provided, returns the airline with the
        specified code.
        If query parameters are provided, returns a list of airlines that match
        the query parameters.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """

        airline_code = get_param('code', request)

        if airline_code:
            try:
                airline = Airline.objects.get(code=airline_code)
            except Airline.DoesNotExist:
                return Response(
                    {"error": f'Airline with code {airline_code} does not exist'},
                    status=status.HTTP_404_NOT_FOUND)

            serializer = AirlineSerializer(airline)
            return Response(serializer.data, status=status.HTTP_200_OK)

        airlines = Airline.objects.all()
        serializer = AirlineSerializer(airlines, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AirportViewSet(viewsets.GenericViewSet):
    """Viewset for the Airport model."""

    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AirportFilter

    @action(detail=False, methods=['get'], serializer_class=AirportSerializer)
    def get_airports(self, request):
        """
        Returns a list of all airports, or a specific airport if an ident is provided.
        The ident can be provided as a query parameter, or in the request.

        Users can filter airports based on query parameters. For example:

        - `/api/airports/?city=New York`
        - `/api/airports/?country=US`
        - `/api/airports/?region=US-NY`
        - `/api/airports/?type=large_airport`
        - `/api/airports/?latitude_min=40&latitude_max=45`
        - `/api/airports/?longitude_min=-80&longitude_max=-70`
        - `/api/airports/?elevation_min=100&elevation_max=200`
        - `/api/airports/?continent=NA`

        Note that the filtering is case-insensitive and uses the icontains lookup expression for text-based fields, which means it will match any airport containing the specified text. You can change the lookup expression to suit your needs.

        Returns:
            Response: List of all airports, or a specific airport.
        """

        ident = get_param('ident', request)
        name = get_param('name', request)

        if ident and name:
            # If does not exist, return 404
            try:
                airport = Airport.objects.get(ident=ident, name=name)
                # Return the airport
                return Response(AirportSerializer(airport).data, status=status.HTTP_200_OK)
            except Airport.DoesNotExist:
                return Response({'error': f'Airport with ident {ident} and name {name} does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            # Serialize the data
            serializer = AirportSerializer(airport)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if ident:
            # If an ident is provided, return the airport with that ident
            try:
                airport = Airport.objects.get(ident=ident)
                return Response(AirportSerializer(airport).data, status=status.HTTP_200_OK)
            except Airport.DoesNotExist:
                return Response({'error': f'Airport with ident {ident} does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

        if name:
            # If an ident is provided, return the airport with that ident
            try:
                airport = Airport.objects.get(name=name)
                return Response(AirportSerializer(airport).data, status=status.HTTP_200_OK)
            except Airport.DoesNotExist:
                return Response({'error': f'Airport with name {name} does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

        # We want to allow the user to get airports based on a query parameter
        # They can choose a specific city, country, region, type, latitude, longitude, elevation, continent
        # They can also choose a range of values for the above parameters
        # including latitude, longitude, and elevation
        # We can use the django filter package to do this
        airports = Airport.objects.all()

        # Filter the airports based on the query parameters
        airports = AirportFilter(request.GET, queryset=airports).qs

        # If no airports are found, return 404
        if not airports:
            return Response({'error': 'No airports found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data
        serializer = AirportSerializer(airports, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FlightViewSet(viewsets.GenericViewSet):
    """Viewset for the Flight model."""

    queryset = Flight.objects.none()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter

    @action(detail=False, methods=['get'], serializer_class=FlightSerializer)
    def get_flights(self, request):
        """
        Returns a list of all flights, or a specific flight if a flight_code is provided.
        The flight_code can be provided as a query parameter, or in the request.

        Users can filter flights based on query parameters. For example:

        - `/api/flights/?departure_airport=LAX&destination_airport=JFK`
        - `/api/flights/?airline=AA&base_price_min=100&base_price_max=300`
        - `/api/flights/?departure_datetime_min=2023-05-01T00:00:00Z&departure_datetime_max=2023-05-31T23:59:59Z`
        - `/api/flights/?departure_datetime_min=2023-05-09&arrival_datetime_max=2023-05-14`

        The filters allow users to search for flights within a range of values for various parameters
        such as departure datetime, arrival datetime, duration time, base price, total seats,
        and available seats. Users can also filter by departure airport, destination airport, and airline.

        Returns:
            Response: List of all flights, or a specific flight.
        """

        flight_code = get_param('flight_code', request)

        # We want to allow the user to get flights based on a query parameter
        # They can choose a a specific departure_datetime, destination_airport, departure_airport, airline, arrival_datetime, duration_time, base_price, total_seats, available_seats
        # They can also choose a range of values for the above parameters
        # including before the arrival datetime, after the departure datetime, etc.
        # We can use the django filter package to do this

        if flight_code:
            # Get the specific flight with the provided flight_code
            flights = Flight.objects.filter(flight_code=flight_code)
            if not flights.exists():
                return Response({"detail": f'Flight \'{flight_code}\' not found.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(flights.first()).data, status=status.HTTP_200_OK)

        # Get filtered flights or all flights if no filter is applied
        flight_filter = FlightFilter(
            request.GET, queryset=Flight.objects.all())

        # Do not show flights with 0 available seats
        flights = flight_filter.qs.filter(available_seats__gt=0)

        if not flights.exists():
            return Response(
                {"detail": "No flights available."},
                status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(flights, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=FlightSerializer)
    def create_flight(self, request):
        """
        Creates a new flight.
        The flight_code can be provided as a query parameter, or in the request.

        Args:
            request (Request): The flight details.

        Returns:
            Response: The response object.
        """

        flight_code = get_param('flight_code', request)

        if not flight_code:
            return Response(
                {"error": "Flight code is required"},
                status=status.HTTP_400_BAD_REQUEST)

        # If flight code exists in the database, return error
        if Flight.objects.filter(flight_code=flight_code).exists():
            return Response(
                {"error": f'Flight \'{flight_code}\' already exists'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if serializer.errors:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'], serializer_class=FlightSerializer)
    def modify_flight(self, request):
        """
        Modifies a flight.
        The flight_code can be provided as a query parameter, or in the request.

        Args:
            request (Request): The flight details.

        Returns:
            Response: The response object.
        """

        flight_code = get_param('flight_code', request)

        if not flight_code:
            return Response(
                {"error": "Flight code is required"},
                status=status.HTTP_400_BAD_REQUEST)

        flight = Flight.objects.filter(flight_code=flight_code).first()
        if not flight:
            return Response({"error": f'Flight \'{flight_code}\' not found'}, status=status.HTTP_404_NOT_FOUND)

        # If flight is the exact same
        if flight == request.data:
            return Response({"detail": "No changes made"}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(
            flight, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": f'Flight \'{flight_code}\' modified'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], serializer_class=FlightSerializer)
    def delete_flight(self, request):
        """
        Deletes a flight.
        The flight_code can be provided as a query parameter, or in the request.

        Args:
            request (Request): The flight code.

        Returns:
            Response: The response object.
        """

        flight_code = get_param('flight_code', request)

        if not flight_code:
            return Response(
                {"error": "Flight code is required"},
                status=status.HTTP_400_BAD_REQUEST)

        flight = Flight.objects.filter(flight_code=flight_code).first()
        if not flight:
            return Response({"error": f'Flight \'{flight_code}\' not found'}, status=status.HTTP_404_NOT_FOUND)

        flight.delete()

        return Response({"detail": f'Flight \'{flight_code}\' deleted'}, status=status.HTTP_200_OK)


class BookingViewSet(viewsets.GenericViewSet):
    """Viewset for the Booking model."""

    queryset = Booking.objects.none()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['get'], serializer_class=BookingSerializer)
    def get_bookings(self, request):
        """
        Returns a list of all bookings, or a specific booking if a booking_ref is provided.
        If a booking_ref is provided, it can be provided as a query parameter, or in the request.

        Returns:
            Response: List of all bookings, or a specific booking.
        """
        
        booking_ref = get_param('booking_ref', request)

        if booking_ref:
            # Get the specific booking with the provided booking_ref
            bookings = Booking.objects.filter(booking_ref=booking_ref)
            if not bookings.exists():
                return Response({"detail": f'Booking \'{booking_ref}\' not found.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(bookings.first()).data, status=status.HTTP_200_OK)

        flight_code = get_param('flight', request)
        passport_number = get_param('passport_number', request)

        if flight_code:
            # Get the specific booking with the provided flight_code
            # but if passport_number is provided, use it in query as well
            if passport_number:
                bookings = Booking.objects.filter(
                    flight=flight_code, passport_number=passport_number)
                if not bookings.exists():
                    return Response({
                        "detail": f'No bookings found with flight code \'{flight_code}\' and passport number \'{passport_number}\'.'},
                        status=status.HTTP_404_NOT_FOUND)
            else:
                bookings = Booking.objects.filter(flight=flight_code)
                if not bookings.exists():
                    return Response({"detail": f'No bookings found with flight code \'{flight_code}\'.'},
                                    status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(bookings.first()).data, status=status.HTTP_200_OK)

        if passport_number:
            # Get the specific bookings with the provided passport_number
            bookings = Booking.objects.filter(passport_number=passport_number)
            if not bookings.exists():
                return Response({"detail": f'No bookings found with passport number \'{passport_number}\'.'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(bookings.first()).data, status=status.HTTP_200_OK)

        # Otherwise get all bookings
        bookings = Booking.objects.all()
        if not bookings.exists():
            return Response(
                {"detail": "No bookings available."},
                status=status.HTTP_204_NO_CONTENT)
        return Response(self.get_serializer(bookings, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=BookingSerializer)
    def create_booking(self, request):
        """Creates a new booking.

        Args:
            request (Request): The booking details.

        Returns:
            Response: The response object.
        """

        booking_ref = get_param('booking_ref', request)
        flight_code = get_param('flight', request)
        passport_number = get_param('passport_number', request)

        # If booking_ref is provided, check if it exists
        # If it does, return an error
        if booking_ref:
            booking = Booking.objects.filter(booking_ref=booking_ref).first()
            if booking:
                return Response({"error": f'Booking \'{booking_ref}\' already exists'},
                                status=status.HTTP_400_BAD_REQUEST)

        flight = Flight.objects.filter(flight_code=flight_code).first()
        if not flight:
            return Response({"error": f'Flight \'{flight_code}\' not found'}, status=status.HTTP_404_NOT_FOUND)

        # If passport number and flight is provided and a booking exists with same values then error
        if passport_number:
            booking = Booking.objects.filter(
                flight=flight, passport_number=passport_number).first()
            if booking:
                return Response({
                    "error": f'Booking already exists with flight \'{flight_code}\' and passport number \'{passport_number}\''},
                    status=status.HTTP_400_BAD_REQUEST)

        # Save the booking
        booking = Booking.objects.create(
            passport_number=passport_number,
            flight=flight
        )

        serializer = self.get_serializer(booking)

        # We only actually need to return the booking reference
        # but we return the whole booking object
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'], serializer_class=BookingSerializer)
    def modify_booking(self, request):
        """Modifies a booking.

        Args:
            request (Request): The booking details.

        Returns:
            Response: The response object.
        """

        booking_ref = get_param('booking_ref', request)

        if not booking_ref:
            return Response(
                {"error": "Booking reference is required"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(booking_ref=booking_ref)
        except Booking.DoesNotExist:
            return Response({"error": f'Booking \'{booking_ref}\' not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(
            booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], serializer_class=BookingSerializer)
    def delete_booking(self, request):
        """Deletes a booking.

        Args:
            request (Request): The booking reference.

        Returns:
            Response: The response object.
        """

        booking_ref = get_param('booking_ref', request)
        if not booking_ref:
            return Response(
                {"error": "Booking reference is required"},
                status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.filter(booking_ref=booking_ref).first()
        if not booking:
            return Response({"error": f'Booking \'{booking_ref}\' not found'}, status=status.HTTP_404_NOT_FOUND)

        # Use the flight airline to get flight code and its IP address and post to the flight API
        flight_code = booking.flight.flight_code
        flight = Flight.objects.filter(flight=flight_code).first()
        if not flight:
            return Response({"error": f'Flight \'{flight_code}\' not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the airline IP address
        flight_ip_address = flight.airline.ip

        url = f'http://{flight_ip_address}/api/bookings/?booking_ref={booking_ref}'

        # Make the request data
        data = {
            'booking_ref': booking_ref
        }

        # Make the request
        requests.delete(url, data=data, timeout=5)

        booking.delete()

        return Response({"detail": f'Booking \'{booking_ref}\' deleted'}, status=status.HTTP_200_OK)


class CityViewSet(viewsets.GenericViewSet):
    """This class defines the viewset for the City endpoint."""

    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(detail=False, methods=['get'], serializer_class=CitySerializer)
    def get_cities(self, request):
        """Gets the list of cities.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """

        # Get the query parameters
        city = get_param('name', request)
        country = get_param('country', request)

        if city:
            # Get the specific city with the provided city name
            cities = City.objects.filter(name=city)
            if not cities.exists():
                return Response({"detail": f'City \'{city}\' not found.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(cities.first()).data, status=status.HTTP_200_OK)

        if country:
            # Get the specific cities with the provided country name
            cities = City.objects.filter(country=country)
            if not cities.exists():
                return Response({"detail": f'No cities found in \'{country}\'.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(cities, many=True).data, status=status.HTTP_200_OK)

        # Otherwise get all cities
        cities = City.objects.all()
        if not cities.exists():
            return Response(
                {"detail": "No cities available."},
                status=status.HTTP_204_NO_CONTENT)

        return Response(self.get_serializer(cities, many=True).data, status=status.HTTP_200_OK)


class CountryViewSet(viewsets.GenericViewSet):
    """This class defines the viewset for the Country endpoint."""

    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    @action(detail=False, methods=['get'], serializer_class=CountrySerializer)
    def get_countries(self, request):
        """Gets the list of countries.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object.
        """

        # Get the query parameters
        country = get_param('name', request)
        continent = get_param('continent', request)

        if country:
            # Get the specific country with the provided country name
            countries = Country.objects.filter(name=country)
            if not countries.exists():
                return Response({"detail": f'Country \'{country}\' not found.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(countries.first()).data, status=status.HTTP_200_OK)

        if continent:
            # Get the specific countries with the provided continent name
            countries = Country.objects.filter(continent=continent)
            if not countries.exists():
                return Response({"detail": f'No countries found in \'{continent}\'.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(countries, many=True).data, status=status.HTTP_200_OK)

        # Otherwise get all countries
        countries = Country.objects.all()
        if not countries.exists():
            return Response(
                {"detail": "No countries available."},
                status=status.HTTP_204_NO_CONTENT)

        return Response(self.get_serializer(countries, many=True).data, status=status.HTTP_200_OK)
