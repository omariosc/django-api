# views.py
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Flight
from .serializers import FlightSerializer


@api_view(['POST'])
def get_flights(request):
    flights = Flight.objects.all()
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_on_bookings(request):
    # Implement the logic to update bookings
    pass


@api_view(['POST'])
def update_no_seats(request):
    # Implement the logic to update the number of seats
    pass
