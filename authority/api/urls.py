"""This module is used to define the endpoints for the API."""

from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import AirlineViewSet, AirportViewSet, FlightViewSet, BookingViewSet


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),

    path('api/flights/', FlightViewSet.as_view({
        'get': 'get_flights',
        'post': 'create_flight',
        'patch': 'modify_flight',
        'delete': 'delete_flight',
    }), name='flights'),

    path('api/bookings/', BookingViewSet.as_view({
        'get': 'get_bookings',
        'post': 'create_booking',
        'patch': 'modify_booking',
        'delete': 'delete_booking',
    }), name='bookings'),

    path('api/airlines/', AirlineViewSet.as_view({
        'get': 'get_airlines',
        'post': 'create_airline',
        'patch': 'modify_airline',
        'delete': 'delete_airline',
    }), name='airlines'),

    path('api/airports/', AirportViewSet.as_view({
        'get': 'get_airports',
        'post': 'create_airport',
        'patch': 'modify_airport',
        'delete': 'delete_airport',
    }), name='airports'),
]
