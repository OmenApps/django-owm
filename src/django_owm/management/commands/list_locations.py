"""Management command to list all weather locations."""

from django.apps import apps
from django.core.management.base import BaseCommand

from ...app_settings import OWM_MODEL_MAPPINGS


class Command(BaseCommand):
    """Management command to list all weather locations."""

    help = "List all weather locations."

    def handle(self, *args, **options):
        """Handle the command."""
        WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
        locations = WeatherLocationModel.objects.all()

        if not locations:
            self.stdout.write("No weather locations found.")
            return

        for location in locations:
            self.stdout.write(
                f"ID: {location.id}, Name: {location.name}, Coordinates: ({location.latitude}, {location.longitude})"
            )
