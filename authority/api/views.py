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
        This API endpoint retrieves a list of all airlines or a specific airline, depending on the provided parameters. 

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - code: (optional) The unique code of the airline to be retrieved. 

        Returns:
            Response: A Django REST framework response object. 
                Response data format:
                - If the 'code' parameter is provided and an airline with that code exists:
                    - HTTP status code: 200 (OK)
                    - JSON data: A serialized representation of the airline.
                - If the 'code' parameter is provided and an airline with that code does not exist:
                    - HTTP status code: 404 (Not Found)
                    - JSON data: An error message.
                - If the 'code' parameter is not provided:
                    - HTTP status code: 200 (OK)
                    - JSON data: A serialized list of all airlines. 

        Example usage:
            To get a list of all airlines: GET /api/airlines/
            To get a specific airline: GET /api/airlines/?code=AA
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
        This API endpoint retrieves a list of all airports or specific airports based on provided parameters. 

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - ident: (optional) The unique identifier of the airport to be retrieved.
                - name: (optional) The name of the airport to be retrieved.
                - city: (optional) Filter by city.
                - country: (optional) Filter by country.
                - region: (optional) Filter by region.
                - type: (optional) Filter by airport type.
                - latitude_min and latitude_max: (optional) Filter by latitude range.
                - longitude_min and longitude_max: (optional) Filter by longitude range.
                - elevation_min and elevation_max: (optional) Filter by elevation range.
                - continent: (optional) Filter by continent.

        Returns:
            Response: A Django REST framework response object. 
                Response data format:
                - If the 'ident' and/or 'name' parameter is provided and an airport with those values exists:
                    - HTTP status code: 200 (OK)
                    - JSON data: A serialized representation of the airport.
                - If the 'ident' and/or 'name' parameter is provided and an airport with those values does not exist:
                    - HTTP status code: 404 (Not Found)
                    - JSON data: An error message.
                - If no 'ident' or 'name' parameter is provided:
                    - HTTP status code: 200 (OK)
                    - JSON data: A serialized list of all airports that match the other query parameters.

        Example usage:
            To get a list of all airports: GET /api/airports/
            To get a specific airport by ident: GET /api/airports/?ident=KLGA
            To get a specific airport by name: GET /api/airports/?name=LaGuardia
            To get a list of airports in New York: GET /api/airports/?city=New York
            To get a list of airports in the United States: GET /api/airports/?country=US
            To get a list of airports in North America: GET /api/airports/?continent=NA
            To get a list of large airports: GET /api/airports/?type=large_airport
            To get a list of airports in a latitude range: GET /api/airports/?latitude_min=40&latitude_max=45
            To get a list of airports in a longitude range: GET /api/airports/?longitude_min=-80&longitude_max=-70
            To get a list of airports in an elevation range: GET /api/airports/?elevation_min=100&elevation_max=200
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
        This API endpoint retrieves a list of all flights or specific flights based on provided parameters.

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - flight_code: (optional) The unique code of the flight to be retrieved.
                - departure_airport: (optional) Filter by departure airport.
                - destination_airport: (optional) Filter by destination airport.
                - airline: (optional) Filter by airline.
                - base_price_min and base_price_max: (optional) Filter by base price range.
                - departure_datetime_min and departure_datetime_max: (optional) Filter by departure datetime range.
                - arrival_datetime_min and arrival_datetime_max: (optional) Filter by arrival datetime range.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If the 'flight_code' parameter is provided and a flight with that code exists:
                    - HTTP status code: 200 (OK)
                    - JSON data: A serialized representation of the flight.
                - If the 'flight_code' parameter is provided and a flight with that code does not exist:
                    - HTTP status code: 404 (Not Found)
                    - JSON data: An error message.
                - If no 'flight_code' parameter is provided:
                    - HTTP status code: 200 (OK)
                    - JSON data: A serialized list of all flights that match the other query parameters.
                - If no flights match the provided parameters:
                    - HTTP status code: 204 (No Content)
                    - JSON data: An error message.

        Example usage:
            To get a list of all flights: GET /api/flights/
            To get a specific flight by flight_code: GET /api/flights/?flight_code=AA100
            To get a list of flights from LAX to JFK: GET /api/flights/?departure_airport=LAX&destination_airport=JFK
            To get a list of flights with a base price between $100 and $300: GET /api/flights/?base_price_min=100&base_price_max=300
            To get a list of flights with a departure datetime between 2023-05-01T00:00:00Z and 2023-05-31T23:59:59Z: GET /api/flights/?departure_datetime_min=2023-05-01T00:00:00Z&departure_datetime_max=2023-05-31T23:59:59Z
            To get a list of flights with an arrival datetime between 2023-05-01T00:00:00Z and 2023-05-31T23:59:59Z: GET /api/flights/?arrival_datetime_min=2023-05-01T00:00:00Z&arrival_datetime_max=2023-05-31T23:59:59Z            
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
        This API endpoint creates a new flight with the provided details.

        Parameters:
            request (Request): The Django REST framework request object.
                Body parameters (all required):
                - flight_code: The unique code of the flight.
                - departure_airport: The departure airport of the flight.
                - destination_airport: The destination airport of the flight.
                - airline: The airline of the flight.
                - departure_datetime: The departure datetime of the flight.
                - arrival_datetime: The arrival datetime of the flight.
                - duration_time: The duration time of the flight.
                - base_price: The base price of the flight.
                - total_seats: The total seats available on the flight.
                - available_seats: The available seats on the flight at the time of creation.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If the flight is created successfully:
                    - HTTP status code: 201 (Created)
                    - JSON data: A serialized representation of the new flight.
                - If the flight code already exists:
                    - HTTP status code: 400 (Bad Request)
                    - JSON data: An error message.
                - If the request data is invalid:
                    - HTTP status code: 400 (Bad Request)
                    - JSON data: A list of errors detailing what was wrong with the request data.

        Example usage:
            To create a new flight: POST /api/flights/ with the flight details in the request body.
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
        This API endpoint modifies an existing flight's details with the provided information.

        Parameters:
            request (Request): The Django REST framework request object.
                Body parameters (optional):
                - departure_airport: The departure airport of the flight.
                - destination_airport: The destination airport of the flight.
                - airline: The airline of the flight.
                - departure_datetime: The departure datetime of the flight.
                - arrival_datetime: The arrival datetime of the flight.
                - duration_time: The duration time of the flight.
                - base_price: The base price of the flight.
                - total_seats: The total seats available on the flight.
                - available_seats: The available seats on the flight at the time of modification.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If the flight is modified successfully:
                    - HTTP status code: 200 (OK)
                    - JSON data: A message stating that the flight was modified.
                - If the flight code does not exist:
                    - HTTP status code: 404 (Not Found)
                    - JSON data: An error message.
                - If the request data is the same as the current flight data:
                    - HTTP status code: 204 (No Content)
                    - JSON data: A message stating that no changes were made.
                - If the request data is invalid:
                    - HTTP status code: 400 (Bad Request)
                    - JSON data: A list of errors detailing what was wrong with the request data.

        Example usage:
            To modify an existing flight: PATCH /api/flights/ with the flight code and the new flight details in the request body.
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
        This API endpoint deletes an existing flight based on the provided flight code.

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - flight_code (required): The unique code of the flight to be deleted.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If the flight is deleted successfully:
                    - HTTP status code: 200 (OK)
                    - JSON data: A message stating that the flight was deleted.
                - If the flight code does not exist:
                    - HTTP status code: 404 (Not Found)
                    - JSON data: An error message.
                - If the flight code is not provided:
                    - HTTP status code: 400 (Bad Request)
                    - JSON data: An error message indicating that the flight code is required.

        Example usage:
            To delete a flight: DELETE /api/flights/?flight_code=FLIGHT123
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
        This API endpoint retrieves a list of all bookings or a specific booking based on the provided booking reference,
        flight code, or passport number. 

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - booking_ref: The unique reference of the booking to be retrieved.
                - flight: The unique code of the flight associated with the booking.
                - passport_number: The passport number of the passenger.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If a list of bookings is retrieved:
                    - HTTP status code: 200 (OK)
                    - JSON data: A list of booking objects.
                - If a specific booking is retrieved:
                    - HTTP status code: 200 (OK)
                    - JSON data: A booking object.
                - If no bookings are found:
                    - HTTP status code: 204 (No Content)
                    - JSON data: A message stating that no bookings are available.
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
        """
        This API endpoint creates a new booking with the provided booking details.

        Parameters:
            request (Request): The Django REST framework request object.
                Request body (JSON):
                - booking_ref: The unique reference of the booking.
                - flight: The unique code of the flight associated with the booking.
                - passport_number: The passport number of the passenger.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If the booking is created successfully:
                    - HTTP status code: 201 (Created)
                    - JSON data: The created booking object.
                - If the booking already exists or the flight is not found:
                    - HTTP status code: 400 (Bad Request)
                    - JSON data: An error message.
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
        """
        This API endpoint modifies an existing booking based on the provided booking reference.

        Parameters:
            request (Request): The Django REST framework request object.
                Request body (JSON):
                - booking_ref: The unique reference of the booking to be modified.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If the booking is modified successfully:
                    - HTTP status code: 200 (OK)
                    - JSON data: The modified booking object.
                - If the booking does not exist:
                    - HTTP status code: 404 (Not Found)
                    - JSON data: An error message.
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
        """
        This API endpoint deletes an existing booking based on the provided booking reference.

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - booking_ref: The unique reference of the booking to be deleted.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If the booking is deleted successfully:
                    - HTTP status code: 200 (OK)
                    - JSON data: A message stating that the booking was deleted.
                - If the booking or the flight does not exist:
                    - HTTP status code: 404 (Not Found)
                    - JSON data: An error message.
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
        """
        This API endpoint retrieves a list of all cities or specific cities based on the provided city name or country name.

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - id: The ID of the city to be retrieved.
                - name: The name of the city to be retrieved.
                - country: The name of the country whose cities are to be retrieved.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If a list of cities is retrieved:
                    - HTTP status code: 200 (OK)
                    - JSON data: A list of city objects.
                - If a specific city or cities in a country are retrieved:
                    - HTTP status code: 200 (OK)
                    - JSON data: A city object or a list of city objects.
                - If no cities are found:
                    - HTTP status code: 204 (No Content)
                    - JSON data: A message stating that no cities are available.
        """

        # Get the query parameters
        ident = get_param('id', request)
        city = get_param('name', request)
        country = get_param('country', request)
        
        if ident:
            # Get the specific city with the provided city ID
            cities = City.objects.filter(id=ident)
            if not cities.exists():
                return Response({"detail": f'City with ID \'{ident}\' not found.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.get_serializer(cities.first()).data, status=status.HTTP_200_OK)
        
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
        """
        This API endpoint retrieves a list of all countries or specific countries based on the provided country name or continent name.

        Parameters:
            request (Request): The Django REST framework request object.
                Query parameters:
                - name: The name of the country to be retrieved.
                - continent: The name of the continent whose countries are to be retrieved.

        Returns:
            Response: A Django REST framework response object.
                Response data format:
                - If a list of countries is retrieved:
                    - HTTP status code: 200 (OK)
                    - JSON data: A list of country objects.
                - If a specific country or countries in a continent are retrieved:
                    - HTTP status code: 200 (OK)
                    - JSON data: A country object or a list of country objects.
                - If no countries are found:
                    - HTTP status code: 204 (No Content)
                    - JSON data: A message stating that no countries are available.
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
