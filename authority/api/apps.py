"""This module configures the API app."""

from django.apps import AppConfig


class APIConfig(AppConfig):
    """Configures the API app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
