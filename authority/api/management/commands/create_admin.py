"""Creates an admin user with username \"admin\" and password \"admin\""""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """CCommand to create admin users"""

    help = 'Creates admin users with usernames and passwords \"admin\" and \"ammar\".'

    def handle(self, *args, **options):
        """Creates admin users with usernames and passwords \"admin\" and \"ammar\"."""

        admin = "admin"
        ammar = "ammar"

        for i in [admin, ammar]:
            if not User.objects.filter(username=i).exists():
                User.objects.create_superuser(
                    username=i, email='', password=i)
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully created superuser: {i}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Superuser "{i}" already exists.'))
