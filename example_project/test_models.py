"""Tests for the models in the django_owm app."""

from decimal import Decimal

import pytest
from django.apps import apps
from django.utils import timezone

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS


@pytest.fixture
def weather_location_model():
    """Return the WeatherLocation model."""
    return apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))


@pytest.mark.django_db
def test_create_weather_location(weather_location_model):
    """Test creating a WeatherLocation object."""
    WeatherLocation = weather_location_model
    location = WeatherLocation.objects.create(
        name="Test Location", latitude=40.7128, longitude=-74.0060, timezone="America/New_York"
    )
    assert WeatherLocation.objects.count() == 1
    assert location.name == "Test Location"


@pytest.mark.django_db
def test_create_current_weather(weather_location_model):
    """Test creating a CurrentWeather object."""
    WeatherLocation = weather_location_model
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))
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


@pytest.mark.django_db
def test_weather_location_model(weather_location_model):
    """Test the WeatherLocation model."""
    WeatherLocation = weather_location_model

    location = WeatherLocation.objects.create(
        name="Test Location",
        latitude=Decimal("10.0"),
        longitude=Decimal("20.0"),
        timezone="UTC",
    )

    assert location.name == "Test Location"
    assert location.latitude == Decimal("10.0")
    assert location.longitude == Decimal("20.0")
    assert location.timezone == "UTC"


@pytest.mark.django_db
def test_weather_alert_model(weather_location_model):
    """Test the WeatherAlert model."""
    WeatherLocation = weather_location_model
    WeatherAlert = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherAlert"))

    location = WeatherLocation.objects.create(
        name="Alert Location", latitude=Decimal("10.0"), longitude=Decimal("20.0"), timezone="UTC"
    )

    now = timezone.now()
    alert = WeatherAlert.objects.create(
        location=location,
        sender_name="Test Sender",
        event="Test Event",
        start=now,
        end=now + timezone.timedelta(hours=1),
        description="Test description",
    )

    assert alert.location == location
    assert alert.sender_name == "Test Sender"
    assert alert.event == "Test Event"


@pytest.mark.django_db
def test_daily_weather_moon_phase_description(weather_location_model):
    """Test the moon_phase_description property of DailyWeather model."""
    DailyWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("DailyWeather"))
    WeatherLocation = weather_location_model

    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0)

    # Create instances with different moon phases
    moon_phases = [
        (0, "New Moon"),
        (0.25, "First Quarter"),
        (0.5, "Full Moon"),
        (0.75, "Last Quarter"),
        (0.125, "Waxing Crescent"),
        (0.375, "Waxing Gibbous"),
        (0.625, "Waning Gibbous"),
        (0.875, "Waning Crescent"),
        (1, "New Moon"),
        (1.1, "Unknown"),  # Out of expected range
    ]

    for phase_value, expected_description in moon_phases:
        daily_weather = DailyWeather.objects.create(
            location=location,
            timestamp=timezone.now(),
            moon_phase=phase_value,
            weather_condition_id=800,
            weather_condition_main="Clear",
            weather_condition_description="clear sky",
            weather_condition_icon="01d",
        )
        assert daily_weather.moon_phase_description == expected_description


@pytest.mark.django_db
def test_weather_alert_manager_active(weather_location_model):
    """Test the active method of WeatherAlertManager."""
    WeatherLocation = weather_location_model
    WeatherAlert = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherAlert"))

    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")

    now = timezone.now()
    active_alert = WeatherAlert.objects.create(
        location=location,
        sender_name="Sender",
        event="Active Alert",
        start=now - timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=1),
        description="Active alert description",
    )
    WeatherAlert.objects.create(
        location=location,
        sender_name="Sender",
        event="Expired Alert",
        start=now - timezone.timedelta(hours=2),
        end=now - timezone.timedelta(hours=1),
        description="Expired alert description",
    )

    active_alerts = WeatherAlert.objects.filter(end__gte=now)
    assert list(active_alerts) == [active_alert]
