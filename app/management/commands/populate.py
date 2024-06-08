from django.core.management.base import BaseCommand

from app import models


class Command(BaseCommand):
    help = "Populate fake data"

    def handle(self, *args, **options):
        # Populate code here
        self.stdout.write(self.style.SUCCESS("Successfully populated data"))
