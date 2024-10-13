"""Management command to create a new weather location."""

from decimal import ROUND_HALF_UP
from decimal import Decimal

from django.apps import apps
from django.core.management.base import BaseCommand

from ...app_settings import OWM_MODEL_MAPPINGS


class Command(BaseCommand):
    """Management command to create a new weather location."""

    help = "Create a new weather location by entering a location name, latitude, and longitude."

    def handle(self, *args, **options):
        """Handle the command."""
        WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))

        name = input("Enter location name: ")
        latitude = input("Enter latitude: ")
        longitude = input("Enter longitude: ")

        # Trim the latitude and longitude to 2 decimal places
        latitude = Decimal(latitude).quantize(Decimal("1e-2"), rounding=ROUND_HALF_UP)
        longitude = Decimal(longitude).quantize(Decimal("1e-2"), rounding=ROUND_HALF_UP)

        location = WeatherLocationModel.objects.create(name=name, latitude=latitude, longitude=longitude)

        self.stdout.write(self.style.SUCCESS(f"Successfully created location {location.name!r} with ID {location.id}."))
