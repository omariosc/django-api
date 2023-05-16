"""For running unit tests from the command line."""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to run unit tests."""

    help = 'Runs the unit tests.'

    def handle(self, *args, **options):
        """Runs the unit tests."""

        call_command('test', 'api')
