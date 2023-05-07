"""This module contains the admin configuration for the API."""

from django.contrib import admin
from .models import Airline, Airport, Flight, Booking

# Register your models here.
admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Booking)
