"""Tests for the management commands of the django_owm app."""

from decimal import Decimal

import pytest
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.app_settings import OWM_USE_UUID


@pytest.fixture
def weather_location_model():
    """Fixture to get the WeatherLocation model."""
    return apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))


@pytest.fixture
def sample_location(weather_location_model):
    """Fixture to create a sample WeatherLocation instance."""
    return weather_location_model.objects.create(
        name="Test Location", latitude=Decimal("10.00"), longitude=Decimal("20.00"), timezone="UTC"
    )


@pytest.mark.django_db
def test_manual_weather_fetch_command(capsys, sample_location):
    """Test the manual_weather_fetch command."""
    location_id = str(sample_location.uuid if OWM_USE_UUID else sample_location.id)
    call_command("manual_weather_fetch", location_id)
    captured = capsys.readouterr()
    assert "Successfully fetched weather data for location 'Test Location'" in captured.out


@pytest.mark.django_db
def test_manual_weather_fetch_command_invalid_location(capsys):
    """Test the manual_weather_fetch command with an invalid location ID."""
    invalid_id = "9999" if not OWM_USE_UUID else "00000000-0000-0000-0000-000000000000"
    with pytest.raises(CommandError):
        call_command("manual_weather_fetch", invalid_id)
    captured = capsys.readouterr()
    assert f"Location with ID {invalid_id} does not exist." in captured.err


@pytest.mark.django_db
def test_list_locations_command(capsys, weather_location_model):
    """Test the list_locations command."""
    location1 = weather_location_model.objects.create(
        name="Location 1", latitude=Decimal("10.00"), longitude=Decimal("20.00"), timezone="UTC"
    )
    location2 = weather_location_model.objects.create(
        name="Location 2", latitude=Decimal("30.00"), longitude=Decimal("40.00"), timezone="UTC"
    )

    call_command("list_locations")
    captured = capsys.readouterr()

    assert f"ID: {location1.id}, Name: {location1.name}" in captured.out
    assert f"ID: {location2.id}, Name: {location2.name}" in captured.out


@pytest.mark.django_db
def test_list_locations_command_no_locations(capsys):
    """Test the list_locations command with no locations."""
    call_command("list_locations")
    captured = capsys.readouterr()
    assert "No weather locations found." in captured.out


@pytest.mark.django_db
def test_create_location_command(capsys, weather_location_model, monkeypatch):
    """Test the create_location command."""
    inputs = iter(["New Location", "50.00", "60.00"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    call_command("create_location")
    captured = capsys.readouterr()

    assert "Successfully created location 'New Location'" in captured.out
    assert weather_location_model.objects.filter(name="New Location").exists()


@pytest.mark.django_db
def test_delete_location_command(capsys, sample_location, monkeypatch):
    """Test the delete_location command."""
    monkeypatch.setattr("builtins.input", lambda _: "y")

    call_command("delete_location", str(sample_location.id))
    captured = capsys.readouterr()

    assert f"Successfully deleted location {sample_location.name!r}." in captured.out
    assert not sample_location.__class__.objects.filter(id=sample_location.id).exists()


@pytest.mark.django_db
def test_delete_location_command_cancelled(capsys, sample_location, monkeypatch):
    """Test the delete_location command when deletion is cancelled."""
    monkeypatch.setattr("builtins.input", lambda _: "n")

    call_command("delete_location", str(sample_location.id))
    captured = capsys.readouterr()

    assert "Deletion cancelled." in captured.out
    assert sample_location.__class__.objects.filter(id=sample_location.id).exists()


@pytest.mark.django_db
def test_delete_location_command_invalid_location(capsys):
    """Test the delete_location command with an invalid location ID."""
    invalid_id = 9999
    with pytest.raises(CommandError):
        call_command("delete_location", str(invalid_id))
    captured = capsys.readouterr()
    assert f"Location with ID {invalid_id} does not exist." in captured.err
