"""This module is used to define the endpoints for the API."""

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import AirlineViewSet, AirportViewSet, \
    FlightViewSet, BookingViewSet, CityViewSet, CountryViewSet

urlpatterns = [
    # This path is used to access the API documentation
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # This path is used to access the admin panel
    path('admin/', admin.site.urls),

    # These paths are used to access the endpoints
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

    # These paths are used to access the search capabilities
    path('api/airlines/', AirlineViewSet.as_view({
        'get': 'get_airlines',
    }), name='airlines'),

    path('api/airports/', AirportViewSet.as_view({
        'get': 'get_airports',
    }), name='airports'),

    path('api/cities/', CityViewSet.as_view({
        'get': 'get_cities',
    }), name='cities'),

    path('api/countries/', CountryViewSet.as_view({
        'get': 'get_countries',
    }), name='countries'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
