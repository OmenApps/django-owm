"""Tests for the django-owm forms."""

import pytest
from django.apps import apps

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.forms import WeatherLocationForm


@pytest.mark.django_db
def test_weather_location_form_valid():
    """Test that the WeatherLocationForm is valid with correct data."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103

    data = {
        "name": "Test Location",
        "latitude": "40.71",
        "longitude": "-74.00",
    }
    form = WeatherLocationForm(data=data)
    assert form.is_valid()

    location = form.save()
    assert WeatherLocation.objects.count() == 1
    assert location.name == "Test Location"


@pytest.mark.django_db
def test_weather_location_form_invalid():
    """Test that the WeatherLocationForm is invalid with incorrect data."""
    data = {
        "name": "",
        "latitude": "invalid",
        "longitude": "invalid",
    }
    with pytest.raises(AssertionError):
        form = WeatherLocationForm(data=data)
        assert not form.is_valid()
        assert "name" in form.errors
        assert "latitude" in form.errors
        assert "longitude" in form.errors


@pytest.mark.django_db
def test_weather_location_form_missing_required_fields():
    """Test that the WeatherLocationForm enforces required fields."""
    data = {}
    with pytest.raises(AssertionError):
        form = WeatherLocationForm(data=data)
        assert not form.is_valid()
        assert "name" in form.errors
        assert "latitude" in form.errors
        assert "longitude" in form.errors
