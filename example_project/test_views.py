"""Tests for the views of the django_owm app."""

from decimal import Decimal

import pytest
from django.apps import apps
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils import timezone

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS


@pytest.fixture
def weather_location_model():
    """Return the WeatherLocation model."""
    return apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))


@pytest.fixture
def weather_location_instance(weather_location_model):
    """Fixture to create a WeatherLocation instance."""
    WeatherLocation = weather_location_model
    return WeatherLocation.objects.create(
        name="Test Location", latitude=40.7128, longitude=-74.0060, timezone="America/New_York"
    )


@pytest.fixture
def current_weather(weather_location_instance):
    """Fixture to create a CurrentWeather instance."""
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS["CurrentWeather"])
    return CurrentWeather.objects.create(
        location=weather_location_instance,
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


@pytest.mark.django_db
def test_weather_detail_view(client, weather_location_instance, current_weather):
    """Test the weather_detail view."""
    url = reverse("django_owm:weather_detail", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["location"] == weather_location_instance
    assert response.context["current_weather"] == current_weather


@pytest.mark.django_db
def test_list_locations_view(client, weather_location_model, weather_location_instance):
    """Test the list_locations view."""
    WeatherLocation = weather_location_model
    location2 = WeatherLocation.objects.create(name="Location 2", latitude=30.0, longitude=40.0, timezone="UTC")

    url = reverse("django_owm:list_locations")
    response = client.get(url)

    assert response.status_code == 200
    assert list(response.context["locations"]) == [weather_location_instance, location2]
    assert "Location 2" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_create_location_view(client, weather_location_model):
    """Test the create_location view."""
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
    assert response.status_code == 302
    assert response.url == reverse("django_owm:list_locations")

    WeatherLocation = weather_location_model
    assert WeatherLocation.objects.count() == 1
    assert WeatherLocation.objects.first().name == "New Location"

    # Test POST request with invalid data
    invalid_data = {
        "name": "",
        "latitude": "invalid",
        "longitude": "invalid",
    }
    response = client.post(url, invalid_data)
    assert response.status_code == 200
    assert response.context["form"].errors


@pytest.mark.django_db
def test_delete_location_view(client, weather_location_model, weather_location_instance):
    """Test the delete_location view."""
    url = reverse("django_owm:delete_location", args=[weather_location_instance.id])

    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["location"] == weather_location_instance

    # Test POST request
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse("django_owm:list_locations")

    WeatherLocation = weather_location_model
    assert WeatherLocation.objects.count() == 0


@pytest.mark.django_db
def test_update_location_view(client, weather_location_instance):
    """Test the update_location view."""
    url = reverse("django_owm:update_location", args=[weather_location_instance.id])

    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["form"].instance == weather_location_instance

    # Test POST request with valid data
    data = {
        "name": "Updated Name",
        "latitude": "30.0",
        "longitude": "40.0",
        "timezone": "UTC",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("django_owm:list_locations")

    weather_location_instance.refresh_from_db()
    assert weather_location_instance.name == "Updated Name"
    assert float(weather_location_instance.latitude) == 30.0
    assert float(weather_location_instance.longitude) == 40.0


@pytest.mark.django_db
def test_weather_history_view(client, weather_location_instance, current_weather):
    """Test the weather_history view."""
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))
    weather2 = CurrentWeather.objects.create(
        location=weather_location_instance,
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

    url = reverse("django_owm:weather_history", args=[weather_location_instance.id])
    response = client.get(url)

    assert response.status_code == 200
    assert list(response.context["historical_weather"]) == [current_weather, weather2]


@pytest.mark.django_db
def test_weather_forecast_view(client, weather_location_instance):
    """Test the weather_forecast view."""
    HourlyWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("HourlyWeather"))
    DailyWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("DailyWeather"))

    now = timezone.now()

    hourly_forecast = HourlyWeather.objects.create(
        location=weather_location_instance,
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

    daily_forecast = DailyWeather.objects.create(
        location=weather_location_instance,
        timestamp=now + timezone.timedelta(days=1),
        temp_min=Decimal("295.15"),
        temp_max=Decimal("305.15"),
        weather_condition_id=800,
        weather_condition_main="Clear",
        weather_condition_description="clear sky",
        weather_condition_icon="01d",
    )

    url = reverse("django_owm:weather_forecast", args=[weather_location_instance.id])
    response = client.get(url)

    assert response.status_code == 200
    assert list(response.context["hourly_forecast"]) == [hourly_forecast]
    assert list(response.context["daily_forecast"]) == [daily_forecast]


@pytest.mark.django_db
def test_weather_alerts_view(client, weather_location_instance):
    """Test the weather_alerts view."""
    WeatherAlert = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherAlert"))

    now = timezone.now()

    alert = WeatherAlert.objects.create(
        location=weather_location_instance,
        sender_name="Test Sender",
        event="Test Alert",
        start=now - timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=1),
        description="This is a test alert.",
    )

    url = reverse("django_owm:weather_alerts", args=[weather_location_instance.id])
    response = client.get(url)

    assert response.status_code == 200
    assert list(response.context["alerts"]) == [alert]


@pytest.mark.django_db
def test_weather_errors_view(client, weather_location_instance):
    """Test the weather_errors view."""
    WeatherErrorLog = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))

    error_log = WeatherErrorLog.objects.create(
        location=weather_location_instance,
        api_name="one_call",
        error_message="API rate limit exceeded",
        response_data="{'cod': 429, 'message': 'You have exceeded the API call rate limit.'}",
    )

    url = reverse("django_owm:weather_errors", args=[weather_location_instance.id])
    response = client.get(url)

    assert response.status_code == 200
    assert list(response.context["errors"]) == [error_log]


@pytest.mark.django_db
def test_weather_detail_view_nonexistent_location(client):
    """Test the weather_detail view with a nonexistent location."""
    url = reverse("django_owm:weather_detail", kwargs={"location_id": 9999})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_location_view_invalid_coordinates(client):
    """Test the create_location view with invalid coordinates."""
    url = reverse("django_owm:create_location")
    data = {
        "name": "Invalid Location",
        "latitude": "91.0",  # Invalid latitude
        "longitude": "181.0",  # Invalid longitude
        "timezone": "UTC",
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert "form" in response.context
    assert "latitude" in response.context["form"].errors
    assert "longitude" in response.context["form"].errors


@pytest.mark.django_db
def test_update_location_view_nonexistent_location(client):
    """Test the update_location view with a nonexistent location."""
    url = reverse("django_owm:update_location", args=[9999])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_location_view_nonexistent_location(client):
    """Test the delete_location view with a nonexistent location."""
    url = reverse("django_owm:delete_location", args=[9999])
    response = client.post(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_weather_forecast_view_no_forecast_data(client, weather_location_instance):
    """Test the weather_forecast view with no forecast data."""
    url = reverse("django_owm:weather_forecast", args=[weather_location_instance.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["hourly_forecast"]) == 0
    assert len(response.context["daily_forecast"]) == 0


@pytest.mark.django_db
def test_weather_alerts_view_no_active_alerts(client, weather_location_instance):
    """Test the weather_alerts view with no active alerts."""
    url = reverse("django_owm:weather_alerts", args=[weather_location_instance.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["alerts"]) == 0


@pytest.mark.django_db
def test_weather_errors_view_no_errors(client, weather_location_instance):
    """Test the weather_errors view with no error logs."""
    url = reverse("django_owm:weather_errors", args=[weather_location_instance.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["errors"]) == 0


@pytest.mark.django_db
def test_list_locations_view_empty_database(client, weather_location_model):
    """Test the list_locations view with an empty database."""
    WeatherLocation = weather_location_model
    WeatherLocation.objects.all().delete()
    url = reverse("django_owm:list_locations")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["locations"]) == 0


@pytest.mark.django_db
def test_weather_history_view_large_dataset(client, weather_location_instance):
    """Test the weather_history view with a large dataset."""
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))
    # Create 1000 weather records
    for i in range(1000):
        CurrentWeather.objects.create(
            location=weather_location_instance,
            timestamp=timezone.now() - timezone.timedelta(hours=i),
            temp=Decimal("20.0"),
            feels_like=Decimal("20.0"),
            pressure=1013,
            humidity=50,
            weather_condition_id=800,
            weather_condition_main="Clear",
            weather_condition_description="clear sky",
            weather_condition_icon="01d",
        )
    url = reverse("django_owm:weather_history", args=[weather_location_instance.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["historical_weather"]) == 1000


@pytest.mark.parametrize(
    "invalid_id",
    [
        "abc",  # Non-numeric string
        "123abc",  # Mixed string
        "",  # Empty string
        " ",  # Whitespace
    ],
)
@pytest.mark.django_db
def test_views_with_invalid_location_id(client, invalid_id):
    """Test views with invalid location IDs."""
    views = [
        "django_owm:weather_detail",
        "django_owm:delete_location",
        "django_owm:update_location",
        "django_owm:weather_history",
        "django_owm:weather_forecast",
        "django_owm:weather_alerts",
        "django_owm:weather_errors",
    ]
    for view_name in views:
        with pytest.raises(NoReverseMatch):
            url = reverse(view_name, args=[invalid_id])
            response = client.get(url)
            assert response.status_code in [404, 400], f"Unexpected status code for {view_name} with id '{invalid_id}'"


@pytest.mark.django_db
def test_weather_history_partial(client, weather_location_instance, current_weather):
    """Test the weather_history_partial view."""
    url = reverse("django_owm:weather_history_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "location" in response.context
    assert "page_obj" in response.context
    assert response.context["location"] == weather_location_instance
    assert len(response.context["page_obj"]) > 0


@pytest.mark.django_db
def test_weather_forecast_partial(client, weather_location_instance):
    """Test the weather_forecast_partial view."""
    HourlyWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("HourlyWeather"))
    DailyWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("DailyWeather"))

    # Create some forecast data
    HourlyWeather.objects.create(
        location=weather_location_instance,
        timestamp=timezone.now() + timezone.timedelta(hours=1),
        temp=Decimal("20.0"),
        weather_condition_id=800,
        weather_condition_main="Clear",
    )
    DailyWeather.objects.create(
        location=weather_location_instance,
        timestamp=timezone.now() + timezone.timedelta(days=1),
        temp_min=Decimal("15.0"),
        temp_max=Decimal("25.0"),
        weather_condition_id=800,
        weather_condition_main="Clear",
    )

    url = reverse("django_owm:weather_forecast_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "location" in response.context
    assert "hourly_page_obj" in response.context
    assert "daily_page_obj" in response.context
    assert response.context["location"] == weather_location_instance
    assert len(response.context["hourly_page_obj"]) > 0
    assert len(response.context["daily_page_obj"]) > 0


@pytest.mark.django_db
def test_weather_alerts_partial(client, weather_location_instance):
    """Test the weather_alerts_partial view."""
    WeatherAlert = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherAlert"))

    # Create a weather alert
    WeatherAlert.objects.create(
        location=weather_location_instance,
        sender_name="Test Sender",
        event="Test Alert",
        start=timezone.now(),
        end=timezone.now() + timezone.timedelta(hours=1),
        description="This is a test alert.",
    )

    url = reverse("django_owm:weather_alerts_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "location" in response.context
    assert "page_obj" in response.context
    assert response.context["location"] == weather_location_instance
    assert len(response.context["page_obj"]) > 0


@pytest.mark.django_db
def test_weather_errors_partial(client, weather_location_instance):
    """Test the weather_errors_partial view."""
    WeatherErrorLog = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))

    # Create a weather error log
    WeatherErrorLog.objects.create(
        location=weather_location_instance,
        api_name="test_api",
        error_message="Test error message",
        response_data="{'error': 'Test error'}",
    )

    url = reverse("django_owm:weather_errors_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "location" in response.context
    assert "page_obj" in response.context
    assert response.context["location"] == weather_location_instance
    assert len(response.context["page_obj"]) > 0


@pytest.mark.django_db
def test_weather_history_partial_pagination(client, weather_location_instance):
    """Test pagination in the weather_history_partial view."""
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))

    # Create 10 weather records
    for i in range(10):
        CurrentWeather.objects.create(
            location=weather_location_instance,
            timestamp=timezone.now() - timezone.timedelta(hours=i),
            temp=Decimal("20.0"),
            weather_condition_id=800,
            weather_condition_main="Clear",
        )

    url = reverse("django_owm:weather_history_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "page_obj" in response.context
    assert response.context["page_obj"].paginator.num_pages == 2
    assert len(response.context["page_obj"]) == 5  # 5 items per page


@pytest.mark.django_db
def test_weather_forecast_partial_empty_forecast(client, weather_location_instance):
    """Test the weather_forecast_partial view with no forecast data."""
    url = reverse("django_owm:weather_forecast_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "hourly_page_obj" in response.context
    assert "daily_page_obj" in response.context
    assert len(response.context["hourly_page_obj"]) == 0
    assert len(response.context["daily_page_obj"]) == 0


@pytest.mark.django_db
def test_weather_alerts_partial_no_alerts(client, weather_location_instance):
    """Test the weather_alerts_partial view with no alerts."""
    url = reverse("django_owm:weather_alerts_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "page_obj" in response.context
    assert len(response.context["page_obj"]) == 0


@pytest.mark.django_db
def test_weather_errors_partial_no_errors(client, weather_location_instance):
    """Test the weather_errors_partial view with no error logs."""
    url = reverse("django_owm:weather_errors_partial", kwargs={"location_id": weather_location_instance.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "page_obj" in response.context
    assert len(response.context["page_obj"]) == 0
