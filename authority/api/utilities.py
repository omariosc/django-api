"""This file contains helper functions."""

import random
import string
from api.models import Booking


def generate_booking_ref():
    """Generates a random booking reference.

    Returns:
        str: The booking reference.
    """
    booking_ref = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=10))
    while Booking.objects.filter(booking_ref=booking_ref).exists():
        booking_ref = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

    return booking_ref


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


def validate_airline_code(airline_code):
    if not airline_code:
        return "Airline code is required"
    if len(airline_code) != 3:
        return "Airline code must be 3 characters long"
    return None


def validate_airline_name(airline_name):
    if not airline_name:
        return "Airline name is required"
    return None


def validate_phone(phone):
    if phone:
        if len(phone) != 11:
            return "Phone number must be 11 digits long"
        if not phone.startswith('0'):
            return "Phone number must start with 0"
    return None
