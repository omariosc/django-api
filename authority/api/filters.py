"""This file contains the filters for the Airport and Flight models."""

import django_filters
from api.models import Airport, Flight


class AirportFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name="city", lookup_expr="icontains")
    country = django_filters.CharFilter(
        field_name="country", lookup_expr="icontains")
    iso_country = django_filters.CharFilter(
        field_name="iso_country", lookup_expr="icontains")
    iso_region = django_filters.CharFilter(
        field_name="iso_region", lookup_expr="icontains")
    municipality = django_filters.CharFilter(
        field_name="municipality", lookup_expr="icontains")
    size_type = django_filters.CharFilter(
        field_name="size_type", lookup_expr="icontains")
    latitude_min = django_filters.NumberFilter(
        field_name="latitude", lookup_expr="gte")
    latitude_max = django_filters.NumberFilter(
        field_name="latitude", lookup_expr="lte")
    longitude_min = django_filters.NumberFilter(
        field_name="longitude", lookup_expr="gte")
    longitude_max = django_filters.NumberFilter(
        field_name="longitude", lookup_expr="lte")
    elevation_min = django_filters.NumberFilter(
        field_name="elevation", lookup_expr="gte")
    elevation_max = django_filters.NumberFilter(
        field_name="elevation", lookup_expr="lte")
    continent = django_filters.CharFilter(
        field_name="continent", lookup_expr="icontains")

    class Meta:
        model = Airport
        fields = [
            'city',
            'country',
            'iso_country',
            'iso_region',
            'municipality',
            'size_type',
            'latitude_min',
            'latitude_max',
            'longitude_min',
            'longitude_max',
            'elevation_min',
            'elevation_max',
            'continent',
        ]


class FlightFilter(django_filters.FilterSet):
    """Filters for the Flight model."""

    departure_datetime_min = django_filters.DateTimeFilter(
        field_name="departure_datetime", lookup_expr='gte')
    departure_datetime_max = django_filters.DateTimeFilter(
        field_name="departure_datetime", lookup_expr='lte')
    arrival_datetime_min = django_filters.DateTimeFilter(
        field_name="arrival_datetime", lookup_expr='gte')
    arrival_datetime_max = django_filters.DateTimeFilter(
        field_name="arrival_datetime", lookup_expr='lte')
    duration_time_min = django_filters.DurationFilter(
        field_name="duration_time", lookup_expr='gte')
    duration_time_max = django_filters.DurationFilter(
        field_name="duration_time", lookup_expr='lte')
    base_price_min = django_filters.NumberFilter(
        field_name="base_price", lookup_expr='gte')
    base_price_max = django_filters.NumberFilter(
        field_name="base_price", lookup_expr='lte')
    total_seats_min = django_filters.NumberFilter(
        field_name="total_seats", lookup_expr='gte')
    total_seats_max = django_filters.NumberFilter(
        field_name="total_seats", lookup_expr='lte')
    available_seats_min = django_filters.NumberFilter(
        field_name="available_seats", lookup_expr='gte')
    available_seats_max = django_filters.NumberFilter(
        field_name="available_seats", lookup_expr='lte')

    departure_airport = django_filters.CharFilter(
        field_name="departure_airport__ident", lookup_expr='iexact')
    destination_airport = django_filters.CharFilter(
        field_name="destination_airport__ident", lookup_expr='iexact')
    departure_city = django_filters.CharFilter(
        field_name="departure_airport__city", lookup_expr='iexact')
    destination_city = django_filters.CharFilter(
        field_name="destination_airport__city", lookup_expr='iexact')
    departure_country = django_filters.CharFilter(
        field_name="departure_airport__country", lookup_expr='iexact')
    destination_country = django_filters.CharFilter(
        field_name="destination_airport__country", lookup_expr='iexact')

    class Meta:
        """Meta class for the FlightFilter class."""

        model = Flight
        fields = [
            'departure_airport',
            'destination_airport',
            'airline',
            'departure_datetime_min',
            'departure_datetime_max',
            'arrival_datetime_min',
            'arrival_datetime_max',
            'duration_time_min',
            'duration_time_max',
            'base_price_min',
            'base_price_max',
            'total_seats_min',
            'total_seats_max',
            'available_seats_min',
            'available_seats_max',
            'departure_city',
            'destination_city',
            'departure_country',
            'destination_country',
        ]
