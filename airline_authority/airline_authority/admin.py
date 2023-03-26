from django.contrib import admin
from .models import Airline, Airport, Flight, Booking

admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Booking)
