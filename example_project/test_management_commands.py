"""Tests for the management commands of the django_owm app."""

from io import StringIO

import pytest
from django.apps import apps
from django.core.management import call_command

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.app_settings import OWM_USE_UUID


@pytest.mark.django_db
def test_manual_weather_fetch_command():
    """Test the manual_weather_fetch command."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")

    out = StringIO()
    if OWM_USE_UUID:
        call_command("manual_weather_fetch", location.uuid, stdout=out)
    else:
        call_command("manual_weather_fetch", str(location.id), stdout=out)
    output = out.getvalue()

    assert "Successfully fetched weather data for location" in output


@pytest.mark.django_db
def test_list_locations_command():
    """Test the list_locations command."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    location1 = WeatherLocation.objects.create(name="Location 1", latitude=10.0, longitude=20.0, timezone="UTC")
    location2 = WeatherLocation.objects.create(name="Location 2", latitude=30.0, longitude=40.0, timezone="UTC")

    out = StringIO()
    call_command("list_locations", stdout=out)
    output = out.getvalue()

    assert f"ID: {location1.id}, Name: {location1.name}" in output
    assert f"ID: {location2.id}, Name: {location2.name}" in output


@pytest.mark.django_db
def test_create_location_command(monkeypatch):
    """Test the create_location command."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103

    inputs = iter(["Test Location", "50.0", "60.0", "UTC"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    out = StringIO()
    call_command("create_location", stdout=out)
    output = out.getvalue()

    assert "Successfully created location 'Test Location'" in output
    assert WeatherLocation.objects.count() == 1


@pytest.mark.django_db
def test_delete_location_command(monkeypatch):
    """Test the delete_location command."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    location = WeatherLocation.objects.create(name="Delete Me", latitude=10.0, longitude=20.0, timezone="UTC")

    inputs = iter(["y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    out = StringIO()
    call_command("delete_location", str(location.id), stdout=out)
    output = out.getvalue()

    assert f"Successfully deleted location '{location.name}'." in output
    assert WeatherLocation.objects.count() == 0
