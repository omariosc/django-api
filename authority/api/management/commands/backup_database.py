"""This file contains the command to back up the database."""

import os
import shutil
from datetime import datetime
from io import StringIO
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    """Command to back up the database."""

    help = 'Backs up the database.'

    def handle(self, *args, **options):
        """Backs up the database."""

        # Define backup directory and filename
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Create the backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Copy the database file to the backup directory
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
            db_file = settings.DATABASES['default']['NAME']
            shutil.copy(db_file, backup_file)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully backed up the database to {backup_file}'))
        else:
            # dumpdata api --indent 4 > db.json # MySQL
            backup_file = f'db_backup_{timestamp}.json'
            output = StringIO()
            call_command('dumpdata', 'api', '--indent=4', stdout=output)

            # Write the output of dumpdata to file
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(output.getvalue())
                output.close()

            self.stdout.write(self.style.SUCCESS(
                f'Successfully backed up the database to {backup_file}'))
