"""Management command to manually fetch weather data for a specific location."""

from decimal import Decimal

from django.apps import apps
from django.core.management.base import BaseCommand

from ...app_settings import OWM_MODEL_MAPPINGS
from ...app_settings import OWM_USE_UUID
from ...tasks import fetch_weather


class Command(BaseCommand):
    """Management command to manually fetch weather data for a specific location."""

    help = "Manually fetch weather data for a specific location."

    def add_arguments(self, parser):
        """Add arguments to the command."""
        if OWM_USE_UUID:
            parser.add_argument("location_id", type=Decimal, help="ID of the location to fetch weather for")
        else:
            parser.add_argument("location_id", type=int, help="ID of the location to fetch weather for")

    def handle(self, *args, **options):
        """Handle the command."""
        location_id = options["location_id"]
        WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103

        try:
            location = WeatherLocationModel.objects.get(pk=location_id)
        except WeatherLocationModel.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Location with ID {location_id} does not exist."))
            return

        # Fetch weather data for the specific location
        fetch_weather(location_ids=[location_id])

        self.stdout.write(self.style.SUCCESS(f"Successfully fetched weather data for location '{location.name}'."))
