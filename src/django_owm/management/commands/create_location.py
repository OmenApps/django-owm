"""Management command to create a new weather location."""

from django.apps import apps
from django.core.management.base import BaseCommand

from ...app_settings import OWM_MODEL_MAPPINGS


class Command(BaseCommand):
    """Management command to create a new weather location."""

    help = "Create a new weather location."

    def handle(self, *args, **options):
        """Handle the command."""
        WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103

        name = input("Enter location name: ")
        latitude = input("Enter latitude: ")
        longitude = input("Enter longitude: ")
        timezone = input("Enter timezone (optional): ")

        location = WeatherLocationModel.objects.create(
            name=name, latitude=latitude, longitude=longitude, timezone=timezone if timezone else None
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully created location '{location.name}' with ID {location.id}."))
