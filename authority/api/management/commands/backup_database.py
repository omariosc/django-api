"""This file contains the command to back up the database."""

import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Command to back up the database."""

    help = 'Backs up the database.'

    def handle(self, *args, **options):
        """Backs up the database."""

        # We only backup if the database is SQLite3
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            self.stdout.write(self.style.ERROR(
                'Only SQLite3 backups are supported in this script.'))
            return

        # Define backup directory and filename
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = os.path.join(
            backup_dir, f'db_backup_{timestamp}.sqlite3')

        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Copy the database file to the backup directory
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            db_file = settings.DATABASES['default']['NAME']
            shutil.copy(db_file, backup_file)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully backed up the database to {backup_file}'))
        else:
            self.stdout.write(self.style.ERROR(
                'Only SQLite3 backups are supported in this script.'))
