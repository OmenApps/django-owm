"""Tests for utility functions in the django_owm app."""

import pytest
import requests

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.app_settings import get_model_from_string
from src.django_owm.utils.api import make_api_call
from src.django_owm.utils.saving import save_weather_data


def test_make_api_call_success(monkeypatch):
    """Test that make_api_call returns data when API call is successful."""

    class MockResponse:
        """Mock response object."""

        status_code = 200

        def json(self):
            """Return a test JSON response."""
            return {"data": "test"}

    def mock_get(*args, **kwargs):
        """Mock requests.get to return a successful response."""
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    data = make_api_call(10.0, 20.0)
    assert data == {"data": "test"}


def test_make_api_call_api_error(monkeypatch, caplog):
    """Test that make_api_call handles API errors gracefully."""

    class MockResponse:
        """Mock response object."""

        status_code = 500

        def raise_for_status(self):
            """Raise an HTTPError."""
            raise requests.HTTPError("500 Server Error")

    def mock_get(*args, **kwargs):
        """Mock requests.get to return an error response."""
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    data = make_api_call(10.0, 20.0)
    assert data is None
    # assert "Error fetching weather data" in caplog.text


# def test_make_api_call_missing_api_key(monkeypatch, caplog):
#     """Test that make_api_call logs an error when API key is missing."""
#     # monkeypatch.setattr("src.django_owm.app_settings", "OWM_API_KEY", "")
#     from example_project import settings as example_project_settings
#     monkeypatch.setattr(example_project_settings, "OWM_API_KEY", "")
#     data = make_api_call(10.0, 20.0)
#     assert data is None
#     assert "OpenWeatherMap API key not set" in caplog.text


@pytest.mark.django_db
def test_save_weather_data():
    """Test that save_weather_data saves data correctly."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    CurrentWeather = get_model_from_string(OWM_MODEL_MAPPINGS["CurrentWeather"])  # pylint: disable=C0103

    location = WeatherLocation.objects.create(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")

    data = {
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
        }
    }

    save_weather_data(location, data)

    # Verify that the current weather was saved
    assert CurrentWeather.objects.count() == 1
    weather = CurrentWeather.objects.first()
    assert weather.location == location
    assert float(weather.temp) == 295.15


def test_save_weather_data_missing_data():
    """Test that save_weather_data handles missing data gracefully."""

    class MockLocation:
        """Mock location object."""

        id = 1

    location = MockLocation()
    data = {}

    # No exception should be raised
    save_weather_data(location, data)
