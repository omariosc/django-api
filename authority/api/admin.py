"""This module contains the admin configuration for the API."""

from django.contrib import admin
from .forms import FlightAdminForm, BookingAdminForm
from .models import Airline, Airport, City, Country, Flight, Booking

class ReadOnly(admin.ModelAdmin):
    """Admin configuration for the ready only models."""

    def get_readonly_fields(self, request, obj=None):
        """Returns the read only fields.

        Args:
            request (str): The request.
            obj (str, optional): The object. Defaults to None.

        Returns:
            list: The list of read only fields.
        """
        
        return [f.name for f in self.model._meta.fields]

class FlightAdmin(admin.ModelAdmin):
    """Admin configuration for the Flight model."""

    form = FlightAdminForm

    def get_readonly_fields(self, request, obj=None):
        """
        Returns the read only fields.

        Args:
            request (str): The request.
            obj (str, optional): The object. Defaults to None.

        Returns:
            list: The list of read only fields.
        """
        return [f.name for f in self.model._meta.fields]


class BookingAdmin(admin.ModelAdmin):
    """Admin configuration for the Booking model."""

    form = BookingAdminForm
    readonly_fields = ('booking_ref',)


# Register your models here.
admin.site.register(Airline, ReadOnly)
admin.site.register(Airport, ReadOnly)
admin.site.register(City, ReadOnly)
admin.site.register(Country, ReadOnly)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Flight, FlightAdmin)
