"""This module contains the tests for the API."""

from django.core.management import call_command
from django.test import TestCase,RequestFactory
from .views import AirlineViewSet, AirportViewSet, CityViewSet, CountryViewSet, FlightViewSet, BookingViewSet

class SearchCapabilitiesTest(TestCase):
    """Tests for the search capabilities of the API."""
    
    @classmethod
    def setUpTestData(cls):
        """Initialize the test database.
        
        Args:
            cls: The class itself.
        """
        # Delete the existing database and create a new one
        call_command('flush', '--no-input')

        # Populate the database using the populate_database command
        call_command('populate_database')

        # Initialize the test client
        cls.factory = RequestFactory()
        
    def test_get_countries(self):
        """Test the GET request for countries."""
        
        request = self.factory.get('/countries/')
        view = CountryViewSet.as_view({'get': 'get_countries'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_cities(self):
        """Test the GET request for cities."""
        
        request = self.factory.get('/cities/')
        view = CityViewSet.as_view({'get': 'get_cities'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_airlines(self):
        """Test the GET request for airlines."""
        
        request = self.factory.get('/airlines/')
        view = AirlineViewSet.as_view({'get': 'get_airlines'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_airports(self):
        """Test the GET request for airports."""
        
        request = self.factory.get('/airports/')
        view = AirportViewSet.as_view({'get': 'get_airports'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_filter_flights(self):
        """Test the filtering using the GET request for flights."""
        request = self.factory.get('/countries/', {'name': 'US'})
        view = CountryViewSet.as_view({'get': 'get_countries'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_filter_cities(self):
        """Test the filtering using the GET request for cities."""
        
        request = self.factory.get('/cities/', {'name': 'Cururupu'})
        view = CityViewSet.as_view({'get': 'get_cities'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_filter_airlines(self):
        """Test the filtering using the GET request for airlines."""
        
        request = self.factory.get('/airlines/', {'code': 'SL'})
        view = AirlineViewSet.as_view({'get': 'get_airlines'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_get_filter_airports(self):
        """Test the filtering using the GET request for airports."""
        
        request = self.factory.get('/airports/', {'name': 'Archery Park Helipad'})
        view = AirportViewSet.as_view({'get': 'get_airports'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
