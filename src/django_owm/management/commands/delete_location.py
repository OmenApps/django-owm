"""Management command to delete a weather location."""

from django.apps import apps
from django.core.management.base import BaseCommand

from ...app_settings import OWM_MODEL_MAPPINGS


class Command(BaseCommand):
    """Management command to delete a weather location."""

    help = "Delete a weather location."

    def add_arguments(self, parser):
        """Add arguments to the command."""
        parser.add_argument("location_id", type=int, help="ID of the location to delete")

    def handle(self, *args, **options):
        """Handle the command."""
        location_id = options["location_id"]
        WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103

        try:
            location = WeatherLocationModel.objects.get(pk=location_id)
        except WeatherLocationModel.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Location with ID {location_id} does not exist."))
            return

        confirmation = input(f"Are you sure you want to delete location '{location.name}'? (y/N): ")

        if confirmation.lower() == "y":
            location.delete()
            self.stdout.write(self.style.SUCCESS(f"Successfully deleted location '{location.name}'."))
        else:
            self.stdout.write("Deletion cancelled.")
