"""Tests for the celery tasks module."""

import json
from decimal import Decimal

import pytest
import requests

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.app_settings import get_model_from_string
from src.django_owm.tasks import fetch_weather


@pytest.mark.django_db
def test_fetch_weather(monkeypatch):
    """Test fetching current weather data."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    CurrentWeather = get_model_from_string(OWM_MODEL_MAPPINGS["CurrentWeather"])  # pylint: disable=C0103
    APICallLog = get_model_from_string(OWM_MODEL_MAPPINGS["APICallLog"])  # pylint: disable=C0103

    location = WeatherLocation.objects.create(
        name="Test Location", latitude=40.7128, longitude=-74.0060, timezone="America/New_York"
    )

    def mock_get(url, *args, **kwargs):  # pylint: disable=W0613
        """Mock the requests.get function."""

        class MockResponse:  # pylint: disable=R0903
            """Mock response object to the requests.get call."""

            status_code = 200

            def json_response(self):
                """Return a mock JSON response."""
                return {
                    "lat": 33.44,
                    "lon": -94.04,
                    "timezone": "America/Chicago",
                    "timezone_offset": -18000,
                    "current": {
                        "dt": 1609459200,
                        "temp": 295.15,
                        "feels_like": 295.15,
                        "pressure": 1013,
                        "humidity": 50,
                        "dew_point": 285.15,
                        "uvi": 0.0,
                        "clouds": 10,
                        "visibility": 10000,
                        "wind_speed": 5.0,
                        "wind_deg": 180,
                        "wind_gust": 7.0,
                        "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
                    },
                    "minutely": [
                        {"dt": 1684929540, "precipitation": 0},
                    ],
                    "hourly": [
                        {
                            "dt": 1684926000,
                            "temp": 292.01,
                            "feels_like": 292.33,
                            "pressure": 1014,
                            "humidity": 91,
                            "dew_point": 290.51,
                            "uvi": 0,
                            "clouds": 54,
                            "visibility": 10000,
                            "wind_speed": 2.58,
                            "wind_deg": 86,
                            "wind_gust": 5.88,
                            "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}],
                            "pop": 0.15,
                        },
                    ],
                    "daily": [
                        {
                            "dt": 1684951200,
                            "sunrise": 1684926645,
                            "sunset": 1684977332,
                            "moonrise": 1684941060,
                            "moonset": 1684905480,
                            "moon_phase": 0.16,
                            "summary": "Expect a day of partly cloudy with rain",
                            "temp": {
                                "day": 299.03,
                                "min": 290.69,
                                "max": 300.35,
                                "night": 291.45,
                                "eve": 297.51,
                                "morn": 292.55,
                            },
                            "feels_like": {"day": 299.21, "night": 291.37, "eve": 297.86, "morn": 292.87},
                            "pressure": 1016,
                            "humidity": 59,
                            "dew_point": 290.48,
                            "wind_speed": 3.98,
                            "wind_deg": 76,
                            "wind_gust": 8.92,
                            "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}],
                            "clouds": 92,
                            "pop": 0.47,
                            "rain": 0.15,
                            "uvi": 9.23,
                        },
                    ],
                    "alerts": [
                        {
                            "sender_name": (
                                "NWS Philadelphia - Mount Holly (New Jersey, Delaware, Southeastern Pennsylvania)"
                            ),
                            "event": "Small Craft Advisory",
                            "start": 1684952747,
                            "end": 1684988747,
                            "description": (
                                "...SMALL CRAFT ADVISORY REMAINS IN EFFECT FROM 5 PM THIS\n"
                                "AFTERNOON TO 3 AM EST FRIDAY...\n"
                                "* WHAT...North winds 15 to 20 kt with gusts up to 25 kt and seas\n"
                                "3 to 5 ft expected.\n"
                                "* WHERE...Coastal waters from Little Egg Inlet to Great Egg\n"
                                "Inlet NJ out 20 nm, Coastal waters from Great Egg Inlet to\n"
                                "Cape May NJ out 20 nm and Coastal waters from Manasquan Inlet\n"
                                "to Little Egg Inlet NJ out 20 nm.\n"
                                "* WHEN...From 5 PM this afternoon to 3 AM EST Friday.\n"
                                "* IMPACTS...Conditions will be hazardous to small craft."
                            ),
                            "tags": [],
                        },
                    ],
                }

            def __init__(self) -> None:
                text = json.dumps(self.json_response())
                self.text = text

        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    # Run the task
    fetch_weather()

    # Check that current weather was saved
    assert CurrentWeather.objects.count() == 1
    current_weather = CurrentWeather.objects.first()
    assert current_weather.location == location
    assert current_weather.temp == Decimal("295.15")

    # Check that API call log was created
    assert APICallLog.objects.count() == 1


@pytest.mark.django_db
def test_fetch_weather_api_error(monkeypatch):
    """Test that API errors are handled and logged."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    WeatherErrorLog = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherErrorLog"])  # pylint: disable=C0103

    location = WeatherLocation.objects.create(name="Error Location", latitude=10.0, longitude=20.0, timezone="UTC")

    # Mock the API call to raise an exception
    def mock_make_api_call(lat, lon):
        raise requests.RequestException("API error")

    monkeypatch.setattr("src.django_owm.tasks.make_api_call", mock_make_api_call)

    with pytest.raises(requests.RequestException) as exc_info:
        fetch_weather()

        # Verify that an error was logged
        assert "API error" in str(exc_info.value)
        assert WeatherErrorLog.objects.count() == 1
        error_log = WeatherErrorLog.objects.first()
        assert error_log.location == location
        assert error_log.error_message == "Failed to fetch weather data"


@pytest.mark.django_db
def test_fetch_weather_no_locations(monkeypatch):
    """Test that fetch_weather handles no locations gracefully."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    # Ensure there are no locations
    WeatherLocation.objects.all().delete()

    # Use a flag to check if make_api_call is called
    api_call_called = False

    def mock_make_api_call(lat, lon):  # pylint: disable=W0613
        nonlocal api_call_called
        api_call_called = True
        return {}

    monkeypatch.setattr("src.django_owm.tasks.make_api_call", mock_make_api_call)

    fetch_weather()

    # Ensure that the API was not called
    assert not api_call_called


@pytest.mark.django_db
def test_fetch_weather_exception_handling(monkeypatch, caplog):
    """Test that fetch_weather handles exceptions gracefully."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    WeatherLocation.objects.create(name="Exception Location", latitude=10.0, longitude=20.0, timezone="UTC")

    def mock_make_api_call(lat, lon):
        raise Exception("Test exception")  # pylint: disable=W0719

    monkeypatch.setattr("src.django_owm.tasks.make_api_call", mock_make_api_call)

    with pytest.raises(Exception) as exc_info:
        fetch_weather()
        assert "Test exception" in str(exc_info.value)
