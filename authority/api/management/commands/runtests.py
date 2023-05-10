from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs the unit tests.'

    def handle(self, *args, **options):
        call_command('test', 'api')
