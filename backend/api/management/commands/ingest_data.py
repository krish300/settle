from django.core.management.base import BaseCommand, CommandError

# pylint: disable=import-error
from api import models


class Command(BaseCommand):
    help = 'Ingest the initial data for models'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Started data ingestion...'))
        except Exception:
            raise CommandError('Error occured')

        self.stdout.write(self.style.SUCCESS('Data ingestion complete.'))
