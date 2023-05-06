# views.py
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Flight


@api_view(['POST'])
def flights(request):
    pass


@api_view(['POST'])
def bookings(request):
    pass
