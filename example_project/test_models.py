"""Tests for the models in the django_owm app."""

from decimal import Decimal

import pytest
from django.utils import timezone

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.app_settings import get_model_from_string


@pytest.mark.django_db
def test_create_weather_location():
    """Test creating a WeatherLocation object."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    location = WeatherLocation.objects.create(
        name="Test Location", latitude=40.7128, longitude=-74.0060, timezone="America/New_York"
    )
    assert WeatherLocation.objects.count() == 1
    assert location.name == "Test Location"


@pytest.mark.django_db
def test_create_current_weather():
    """Test creating a CurrentWeather object."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    CurrentWeather = get_model_from_string(OWM_MODEL_MAPPINGS["CurrentWeather"])  # pylint: disable=C0103
    location = WeatherLocation.objects.create(
        name="Test Location", latitude=40.7128, longitude=-74.0060, timezone="America/New_York"
    )

    current_weather = CurrentWeather.objects.create(
        location=location,
        timestamp=timezone.now(),
        temp=Decimal("295.15"),
        feels_like=Decimal("295.15"),
        pressure=1013,
        humidity=50,
        dew_point=Decimal("285.15"),
        uvi=Decimal("0.0"),
        clouds=10,
        visibility=10000,
        wind_speed=Decimal("5.0"),
        wind_deg=180,
        wind_gust=Decimal("7.0"),
        rain_1h=0.0,
        snow_1h=0.0,
        weather_condition_id=800,
        weather_condition_main="Clear",
        weather_condition_description="clear sky",
        weather_condition_icon="01d",
    )
    assert CurrentWeather.objects.count() == 1
    assert current_weather.location == location
