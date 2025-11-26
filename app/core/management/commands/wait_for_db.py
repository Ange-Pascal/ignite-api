"""
Custom Django management command to wait for the database to be available.
"""

import time

from psycopg import OperationalError as Psycopg3Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command that waits until the database is ready."""

    def handle(self, *args, **options):
        """Entrypoint for the command."""
        self.stdout.write("Waiting for database...")

        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg3Error, OperationalError):
                self.stdout.write(
                    "Database unavailable, waiting 1 second..."
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
