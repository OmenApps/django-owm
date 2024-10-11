"""Tests for the views of the django_owm app."""

from decimal import Decimal

import pytest
from django.apps import apps
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.app_settings import get_model_from_string


@pytest.mark.django_db
def test_weather_detail_view():
    """Test the weather_detail view."""
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
        weather_condition_id=800,
        weather_condition_main="Clear",
        weather_condition_description="clear sky",
        weather_condition_icon="01d",
    )

    client = Client()
    url = reverse("django_owm:weather_detail", kwargs={"location_id": location.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "location" in response.context
    assert response.context["location"] == location
    assert "current_weather" in response.context
    assert response.context["current_weather"] == current_weather


@pytest.mark.django_db
def test_list_locations_view():
    """Test the list_locations view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103

    # Create test locations
    location1 = WeatherLocation.objects.create(name="Location 1", latitude=10.0, longitude=20.0, timezone="UTC")
    location2 = WeatherLocation.objects.create(name="Location 2", latitude=30.0, longitude=40.0, timezone="UTC")

    client = Client()
    url = reverse("django_owm:list_locations")
    response = client.get(url)

    assert response.status_code == 200
    assert "locations" in response.context
    assert list(response.context["locations"]) == [location1, location2]
    content = response.content.decode("utf-8")
    assert "Location 1" in content
    assert "Location 2" in content


@pytest.mark.django_db
def test_create_location_view():
    """Test the create_location view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103

    client = Client()
    url = reverse("django_owm:create_location")

    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context

    # Test POST request with valid data
    data = {
        "name": "New Location",
        "latitude": "50.0",
        "longitude": "60.0",
        "timezone": "UTC",
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirects after successful creation
    assert response.url == reverse("django_owm:list_locations")

    # Verify that the location was created
    assert WeatherLocation.objects.count() == 1
    location = WeatherLocation.objects.first()
    assert location.name == "New Location"

    # Test POST request with invalid data
    invalid_data = {
        "name": "",  # Name is required
        "latitude": "invalid",  # Should be a decimal
        "longitude": "invalid",
    }
    response = client.post(url, invalid_data)
    assert response.status_code == 200  # Should return to form with errors
    assert "form" in response.context
    assert response.context["form"].errors


@pytest.mark.django_db
def test_delete_location_view():
    """Test the delete_location view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    location = WeatherLocation.objects.create(name="Location to Delete", latitude=10.0, longitude=20.0, timezone="UTC")

    client = Client()
    url = reverse("django_owm:delete_location", args=[location.id])

    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert "location" in response.context
    assert response.context["location"] == location

    # Test POST request
    response = client.post(url)
    assert response.status_code == 302  # Redirects after deletion
    assert response.url == reverse("django_owm:list_locations")

    # Verify that the location was deleted
    assert WeatherLocation.objects.count() == 0


@pytest.mark.django_db
def test_update_location_view():
    """Test the update_location view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    location = WeatherLocation.objects.create(name="Old Name", latitude=10.0, longitude=20.0, timezone="UTC")

    client = Client()
    url = reverse("django_owm:update_location", args=[location.id])

    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].instance == location

    # Test POST request with valid data
    data = {
        "name": "Updated Name",
        "latitude": "30.0",
        "longitude": "40.0",
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirects after successful update
    assert response.url == reverse("django_owm:list_locations")

    # Verify that the location was updated
    location.refresh_from_db()
    assert location.name == "Updated Name"
    assert float(location.latitude) == 30.0
    assert float(location.longitude) == 40.0


@pytest.mark.django_db
def test_weather_history_view():
    """Test the weather_history view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))  # pylint: disable=C0103

    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")

    # Create historical weather data
    weather1 = CurrentWeather.objects.create(
        location=location,
        timestamp=timezone.now() - timezone.timedelta(hours=1),
        temp=Decimal("295.15"),
        feels_like=Decimal("295.15"),
        pressure=1013,
        humidity=50,
        weather_condition_id=800,
        weather_condition_main="Clear",
        weather_condition_description="clear sky",
        weather_condition_icon="01d",
    )
    weather2 = CurrentWeather.objects.create(
        location=location,
        timestamp=timezone.now() - timezone.timedelta(hours=2),
        temp=Decimal("290.15"),
        feels_like=Decimal("290.15"),
        pressure=1010,
        humidity=60,
        weather_condition_id=801,
        weather_condition_main="Clouds",
        weather_condition_description="few clouds",
        weather_condition_icon="02d",
    )

    client = Client()
    url = reverse("django_owm:weather_history", args=[location.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "historical_weather" in response.context
    assert list(response.context["historical_weather"]) == [weather1, weather2]


@pytest.mark.django_db
def test_weather_forecast_view():
    """Test the weather_forecast view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    HourlyWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("HourlyWeather"))  # pylint: disable=C0103
    DailyWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("DailyWeather"))  # pylint: disable=C0103

    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")

    now = timezone.now()

    # Create future hourly forecast
    hourly_forecast = HourlyWeather.objects.create(
        location=location,
        timestamp=now + timezone.timedelta(hours=1),
        temp=Decimal("298.15"),
        feels_like=Decimal("298.15"),
        pressure=1015,
        humidity=55,
        weather_condition_id=800,
        weather_condition_main="Clear",
        weather_condition_description="clear sky",
        weather_condition_icon="01d",
    )

    # Create future daily forecast
    daily_forecast = DailyWeather.objects.create(
        location=location,
        timestamp=now + timezone.timedelta(days=1),
        temp_min=Decimal("295.15"),
        temp_max=Decimal("305.15"),
        weather_condition_id=800,
        weather_condition_main="Clear",
        weather_condition_description="clear sky",
        weather_condition_icon="01d",
    )

    client = Client()
    url = reverse("django_owm:weather_forecast", args=[location.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "hourly_forecast" in response.context
    assert list(response.context["hourly_forecast"]) == [hourly_forecast]
    assert "daily_forecast" in response.context
    assert list(response.context["daily_forecast"]) == [daily_forecast]


@pytest.mark.django_db
def test_weather_alerts_view():
    """Test the weather_alerts view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    WeatherAlert = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherAlert"))  # pylint: disable=C0103

    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")

    now = timezone.now()

    # Create an active alert
    alert = WeatherAlert.objects.create(
        location=location,
        sender_name="Test Sender",
        event="Test Alert",
        start=now - timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=1),
        description="This is a test alert.",
    )

    client = Client()
    url = reverse("django_owm:weather_alerts", args=[location.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "alerts" in response.context
    assert list(response.context["alerts"]) == [alert]


@pytest.mark.django_db
def test_weather_errors_view():
    """Test the weather_errors view."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    WeatherErrorLog = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))  # pylint: disable=C0103

    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")

    # Create an error log
    error_log = WeatherErrorLog.objects.create(
        location=location,
        api_name="one_call",
        error_message="API rate limit exceeded",
        response_data="{'cod': 429, 'message': 'You have exceeded the API call rate limit.'}",
    )

    client = Client()
    url = reverse("django_owm:weather_errors", args=[location.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "errors" in response.context
    assert list(response.context["errors"]) == [error_log]
