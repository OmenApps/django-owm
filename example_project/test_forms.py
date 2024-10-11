"""Tests for the django_owm forms."""

from decimal import Decimal

import pytest
from django.apps import apps

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.forms import WeatherLocationForm
from src.django_owm.forms import quantize_to_2_decimal_places


@pytest.fixture
def weather_location_model():
    """Return the WeatherLocation model."""
    return apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))


@pytest.fixture
def form_data():
    """Return valid form data."""
    return {"name": "Test Location", "latitude": "32.28", "longitude": "-78.60"}


@pytest.mark.django_db
def test_weather_location_form_valid(form_data, weather_location_model):
    """Test that the WeatherLocationForm is valid with correct data."""
    form = WeatherLocationForm(data=form_data)
    assert form.is_valid()

    location = form.save()
    assert weather_location_model.objects.count() == 1
    assert location.name == "Test Location"
    assert location.latitude == Decimal("32.28")
    assert location.longitude == Decimal("-78.60")


@pytest.mark.parametrize(
    "latitude,expected",
    [
        ("32.001", "32.00"),
        ("32.005", "32.01"),
        ("32.999", "33.00"),
        ("-32.001", "-32.00"),
        ("-32.005", "-32.01"),
    ],
)
def test_latitude_trimming(form_data, latitude, expected):
    """Test that the latitude field is trimmed to 2 decimal places."""
    form_data["latitude"] = latitude
    form = WeatherLocationForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data["latitude"] == Decimal(expected)


@pytest.mark.parametrize(
    "longitude,expected",
    [
        ("-78.001", "-78.00"),
        ("-78.005", "-78.01"),
        ("-78.999", "-79.00"),
        ("78.001", "78.00"),
        ("78.005", "78.01"),
    ],
)
def test_longitude_trimming(form_data, longitude, expected):
    """Test that the longitude field is trimmed to 2 decimal places."""
    form_data["longitude"] = longitude
    form = WeatherLocationForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data["longitude"] == Decimal(expected)


def test_name_not_required(form_data):
    """Test that the name field is not required."""
    del form_data["name"]
    form = WeatherLocationForm(data=form_data)
    assert form.is_valid()


@pytest.mark.parametrize(
    "invalid_latitude",
    [
        "invalid",
        "",
        None,
        "90.01",
        "-90.01",
    ],
)
def test_invalid_latitude(form_data, invalid_latitude):
    """Test that the WeatherLocationForm is invalid with incorrect latitude."""
    form_data["latitude"] = invalid_latitude
    form = WeatherLocationForm(data=form_data)
    assert not form.is_valid()
    assert "latitude" in form.errors


@pytest.mark.parametrize(
    "invalid_longitude",
    [
        "invalid",
        "",
        None,
        "180.01",
        "-180.01",
    ],
)
def test_invalid_longitude(form_data, invalid_longitude):
    """Test that the WeatherLocationForm is invalid with incorrect longitude."""
    form_data["longitude"] = invalid_longitude
    form = WeatherLocationForm(data=form_data)
    assert not form.is_valid()
    assert "longitude" in form.errors


def test_weather_location_form_missing_required_fields():
    """Test that the WeatherLocationForm enforces required fields."""
    form = WeatherLocationForm(data={})
    assert not form.is_valid()
    assert "latitude" in form.errors
    assert "longitude" in form.errors


@pytest.mark.parametrize(
    "value,expected",
    [
        (Decimal("1.234"), Decimal("1.23")),
        (Decimal("1.235"), Decimal("1.24")),
        ("1.234", Decimal("1.23")),
        ("1.235", Decimal("1.24")),
        (None, None),
    ],
)
def test_quantize_to_2_decimal_places(value, expected):
    """Test the quantize_to_2_decimal_places function."""
    result = quantize_to_2_decimal_places(value)
    assert result == expected


def test_quantize_to_2_decimal_places_invalid_input():
    """Test the quantize_to_2_decimal_places function with invalid input."""
    with pytest.raises(ValueError):
        quantize_to_2_decimal_places(1.23)


@pytest.mark.django_db
def test_weather_location_form_update(weather_location_model, form_data):
    """Test updating an existing WeatherLocation instance."""
    instance = weather_location_model.objects.create(**form_data)
    updated_data = form_data.copy()
    updated_data.update({"name": "Updated Location", "latitude": "40.71", "longitude": "-74.01"})
    form = WeatherLocationForm(data=updated_data, instance=instance)
    assert form.is_valid()
    updated_instance = form.save()
    assert updated_instance.name == "Updated Location"
    assert updated_instance.latitude == Decimal("40.71")
    assert updated_instance.longitude == Decimal("-74.01")
