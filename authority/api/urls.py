"""This module is used to define the endpoints for the API."""

from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.core.management import call_command
from .views import FlightViewSet, BookingViewSet, PassengersPerAirlineToday, FlightIncomeData

# Create admin users 'admin' and 'ammar' if they don't exist
call_command('createadmin')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/flights/', FlightViewSet.as_view({
        'get': 'get_flights',
        'put': 'create_flight',
        'patch': 'modify_flight',
        'delete': 'delete_flight',
    }), name='flights'),
    path('api/bookings/', BookingViewSet.as_view({
        'get': 'get_bookings',
        'put': 'create_booking',
        'patch': 'modify_booking',
        'delete': 'delete_booking',
    }), name='bookings'),
    path('passengers_per_airline_today/',
         PassengersPerAirlineToday.as_view(), name='passengers_per_airline_today'),
    path('flight_income_data/', FlightIncomeData.as_view(),
         name='flight_income_data'),
]
