"""Populates the entire database with airports, airlines, flights, and bookings."""

import os
import csv
import random
from datetime import datetime, timedelta
import django
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from api.models import Airport, Airline, Flight, Booking
from api.utilities import generate_booking_ref

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

django.setup()

AIRPORTS_FILE = 'api/static/data/airports.csv'
AIRPORTS_FILE = 'api/static/data/temp.csv'
NUM_FLIGHTS = 10
NUM_BOOKINGS_PER_FLIGHT = 10


class Command(BaseCommand):
    """Populates the entire database."""

    help = 'Populates the database with sample data'

    def handle(self, *args, **options):
        """Calls the functions to populate the database."""
        self.populate_airlines()
        self.populate_airports(AIRPORTS_FILE)
        self.generate_flights(NUM_FLIGHTS)  # Also generates bookings

    def populate_airlines(self):
        """Populates the airlines table."""

        airlines = {
            'SL': {'code': 'SL', 'name': 'SkyLink', 'country': 'USA',
                   'phone': '+1-800-123-4567', 'ip': 'sc20asb.pythonanywhere.com'},
            'FA': {'code': 'FA', 'name': 'FlyAmmar', 'country': 'Syria',
                   'phone': '+963-555-123456', 'ip': 'sc20amb.pythonanywhere.com'},
            'AS': {'code': 'AS', 'name': 'Airsalka', 'country': 'Syria',
                   'phone': '+963-555-654321', 'ip': 'sc20s2r.pythonanywhere.com'},
            'AA': {'code': 'AA', 'name': 'API Airlines', 'country': 'United Kingdom',
                   'phone': '+44-800-987-6543', 'ip': 'sc20cwb1.pythonanywhere.com'}
        }

        for airline in airlines.values():
            # If airlines already exist, skip them
            if Airline.objects.filter(code=airline['code']).exists():
                self.stdout.write(self.style.WARNING(
                    f'Airline \'{airline["name"]}\' already exists. Skipping...'))
                continue
            try:
                Airline.objects.create(**airline)
                self.stdout.write(self.style.SUCCESS(
                    f'Airline \'{airline["name"]}\' added successfully!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error adding airline \'{airline["name"]}\': {str(e)}'))

    def populate_airports(self, file_path):
        """Populates the airports table."""

        success = 0
        missing = 0
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Only do first 100 lines
            reader = list(reader)[:100]
            for row in reader:
                if not row['id']:
                    missing += 1
                    self.stdout.write(self.style.WARNING(
                        f'Airport \'{row["name"]}\' missing id. Skipping...'))
                    continue
                # If airport already exists by ident or name, skip it
                if Airport.objects.filter(ident=row['ident']).exists() or Airport.objects.filter(name=row['name']).exists():
                    self.stdout.write(self.style.WARNING(
                        f'Airport \'{row["name"]}\' already exists. Skipping...'))
                    continue
                Airport.objects.create(
                    ident=row['ident'],
                    name=row['name'],
                    city=row['municipality'],
                    country=row['iso_country'],
                    iso_country=row['iso_country'],
                    iso_region=row['iso_region'],
                    municipality=row['municipality'],
                    size_type=row['size_type'],
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    elevation=row['elevation'],
                    continent=row['continent'],
                    link=row['link']
                )
                success += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Airport \'{row["name"]}\' added successfully!'))
        self.stdout.write(self.style.SUCCESS(
            f'{success} airports added successfully!'))
        if missing:
            self.stdout.write(self.style.WARNING(
                f'{missing} airports missing id!'))

    def generate_flights(self, num_flights=NUM_FLIGHTS):
        """Generates random flights.

        Args:
            num_flights (int, optional): Number of flights to generate. Defaults to NUM_FLIGHTS.
        """
        airports = list(Airport.objects.all())
        airlines = list(Airline.objects.all())

        for _ in range(num_flights):
            departure_airport = random.choice(airports)
            destination_airport = random.choice(airports)
            while departure_airport == destination_airport:
                destination_airport = random.choice(airports)

            flight_code = f"{random.choice(airlines).code}{random.randint(1000000, 9999999)}"

            # If flight code already exists, create a new one
            while Flight.objects.filter(flight_code=flight_code).exists():
                flight_code = f"{random.choice(airlines).code}{random.randint(1000000, 9999999)}"

            departure_datetime = make_aware(
                datetime.now() + timedelta(hours=random.randint(-720, 720)))
            arrival_datetime = departure_datetime + \
                timedelta(minutes=random.randint(60, 1200))
            duration = arrival_datetime - departure_datetime
            base_price = round(random.uniform(10, 10000), 2)
            total_seats = random.randint(10, 500)
            available_seats = random.randint(0, total_seats)
            airline = random.choice(airlines)

            flight = Flight.objects.create(
                departure_airport=departure_airport,
                destination_airport=destination_airport,
                flight_code=flight_code,
                departure_datetime=departure_datetime,
                arrival_datetime=arrival_datetime,
                duration_time=duration,
                base_price=base_price,
                total_seats=total_seats,
                available_seats=available_seats,
                airline=airline
            )

            # Generate bookings based on random number smaller than available seats
            self.generate_bookings(
                flight, random.randint(0, NUM_BOOKINGS_PER_FLIGHT))

    def generate_bookings(self, flight, num_bookings):
        """Generates random bookings.

        Args:
            flight (Flight): The flight to generate bookings for.
            num_bookings (int): Number of bookings to generate.
        """

        created_bookings = 0

        for _ in range(num_bookings):
            # If no more seats available, stop generating bookings
            if flight.available_seats == 0:
                break

            flight.available_seats -= 1
            flight.save()

            Booking.objects.create(
                booking_ref=generate_booking_ref(),
                passport_number=random.randint(10000000, 99999999),
                flight=flight
            )

            created_bookings += 1

        self.stdout.write(self.style.SUCCESS(
            f'{created_bookings} bookings added successfully for flight \'{flight.flight_code}\'!'))