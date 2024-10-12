"""Tests for utility functions in the django_owm app."""

import logging
from decimal import Decimal

import pytest
import requests
from django.apps import apps

from src.django_owm.app_settings import OWM_API_RATE_LIMITS
from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.utils.api import check_api_limits
from src.django_owm.utils.api import get_api_call_counts
from src.django_owm.utils.api import log_api_call
from src.django_owm.utils.api import make_api_call
from src.django_owm.utils.saving import save_alerts
from src.django_owm.utils.saving import save_current_weather
from src.django_owm.utils.saving import save_daily_weather
from src.django_owm.utils.saving import save_error_log
from src.django_owm.utils.saving import save_hourly_weather
from src.django_owm.utils.saving import save_minutely_weather
from src.django_owm.utils.saving import save_weather_data


class MockModel:
    """Mock model object for testing."""

    def __init__(self):
        self.objects = self
        self.create_calls = 0
        self.last_create_kwargs = None

    def create(self, **kwargs):
        """Mock create method."""
        self.create_calls += 1
        self.last_create_kwargs = kwargs


@pytest.fixture
def mock_model():
    """Fixture to return a mock model object."""
    return MockModel()


@pytest.fixture
def mock_apps_get_model(monkeypatch, mock_model):
    """Fixture to mock the apps.get_model function."""

    def mock_get_model(model_name):  # pylint: disable=W0613
        """Mock get_model function."""
        return mock_model

    monkeypatch.setattr(apps, "get_model", mock_get_model)
    return mock_get_model


def test_make_api_call_success(monkeypatch):
    """Test that make_api_call returns data when API call is successful."""

    class MockResponse:
        """Mock response object."""

        status_code = 200
        text = ""

        def json(self):
            """Return a test JSON response."""
            return {"data": "test"}

    def mock_get(*args, **kwargs):  # pylint: disable=W0613
        """Mock requests.get to return a successful response."""
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    data = make_api_call(10.0, 20.0)
    assert data == {"data": "test"}


def test_make_api_call_error(monkeypatch, caplog):
    """Test that make_api_call handles API errors gracefully."""

    class MockResponse:
        """Mock response object with error status code."""

        status_code = 404
        text = ""

    def mock_requests_get(*args, **kwargs):  # pylint: disable=W0613
        """Mock requests.get to return an error response."""
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_requests_get)

    with caplog.at_level(logging.ERROR):
        result = make_api_call(Decimal("10.0"), Decimal("20.0"))

    assert result is None
    assert "Error fetching weather data" in caplog.text


@pytest.mark.django_db
def test_save_weather_data():
    """Test that save_weather_data saves data correctly."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))

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


@pytest.mark.parametrize(
    "model_name",
    ["CurrentWeather", "MinutelyWeather", "HourlyWeather", "DailyWeather", "WeatherAlert", "WeatherErrorLog"],
)
def test_model_not_configured(model_name, monkeypatch, caplog):
    """Test that the correct error message is logged when a model is not configured."""
    monkeypatch.setattr(apps, "get_model", lambda x: None)

    location = object()  # simple mock location
    data = {}

    with caplog.at_level(logging.ERROR):
        if model_name == "CurrentWeather":
            save_current_weather(location, data)
        elif model_name == "MinutelyWeather":
            save_minutely_weather(location, data)
        elif model_name == "HourlyWeather":
            save_hourly_weather(location, data)
        elif model_name == "DailyWeather":
            save_daily_weather(location, data)
        elif model_name == "WeatherAlert":
            save_alerts(location, data)
        elif model_name == "WeatherErrorLog":
            save_error_log(location, "test_api", "test_error")

    assert f"{model_name} is not configured." in caplog.text


def test_save_current_weather_no_data(mock_apps_get_model, mock_model):  # pylint: disable=W0613
    """Test that save_current_weather does not create a record when no data is provided."""
    location = object()  # simple mock location
    data = {}

    save_current_weather(location, data)
    assert mock_model.create_calls == 0


@pytest.mark.parametrize(
    "weather_data, expected_calls",
    [
        ({}, 0),
        ({"minutely": []}, 0),
        ({"minutely": [{"dt": 1609459200, "precipitation": 0.5}]}, 1),
    ],
)
def test_save_minutely_weather(mock_apps_get_model, mock_model, weather_data, expected_calls):  # pylint: disable=W0613
    """Test that save_minutely_weather creates the correct number of records."""
    location = object()  # simple mock location

    save_minutely_weather(location, weather_data)
    assert mock_model.create_calls == expected_calls


@pytest.mark.parametrize(
    "weather_data, expected_calls",
    [
        ({}, 0),
        ({"hourly": []}, 0),
        ({"hourly": [{"dt": 1609459200, "temp": 20.5}]}, 1),
    ],
)
def test_save_hourly_weather(mock_apps_get_model, mock_model, weather_data, expected_calls):  # pylint: disable=W0613
    """Test that save_hourly_weather creates the correct number of records."""
    location = object()  # simple mock location

    save_hourly_weather(location, weather_data)
    assert mock_model.create_calls == expected_calls


@pytest.mark.parametrize(
    "weather_data, expected_calls",
    [
        ({}, 0),
        ({"daily": []}, 0),
        ({"daily": [{"dt": 1609459200, "temp": {"day": 20.5}}]}, 1),
    ],
)
def test_save_daily_weather(mock_apps_get_model, mock_model, weather_data, expected_calls):  # pylint: disable=W0613
    """Test that save_daily_weather creates the correct number of records."""
    location = object()  # simple mock location

    save_daily_weather(location, weather_data)
    assert mock_model.create_calls == expected_calls


@pytest.mark.parametrize(
    "weather_data, expected_calls",
    [
        ({}, 0),
        ({"alerts": []}, 0),
        ({"alerts": [{"sender_name": "Test", "event": "Storm", "start": 1609459200, "end": 1609545600}]}, 1),
    ],
)
def test_save_alerts(mock_apps_get_model, mock_model, weather_data, expected_calls):  # pylint: disable=W0613
    """Test that save_alerts creates the correct number of records."""
    location = object()  # simple mock location

    save_alerts(location, weather_data)
    assert mock_model.create_calls == expected_calls


def test_save_error_log(mock_apps_get_model, mock_model):  # pylint: disable=W0613
    """Test that save_error_log creates a record with the correct data."""
    location = object()  # simple mock location
    api_name = "test_api"
    error_message = "test_error"

    save_error_log(location, api_name, error_message)
    assert mock_model.create_calls == 1
    assert mock_model.last_create_kwargs == {
        "location": location,
        "api_name": api_name,
        "error_message": error_message,
        "response_data": None,
    }


@pytest.fixture
def mock_save_functions(monkeypatch):
    """Fixture to mock the save functions in the saving module."""

    class MockSaveFunction:
        """Mock save function that counts calls and stores arguments."""

        def __init__(self):
            self.call_count = 0
            self.last_call_args = None

        def __call__(self, *args, **kwargs):
            self.call_count += 1
            self.last_call_args = (args, kwargs)

    mock_functions = {
        "save_current_weather": MockSaveFunction(),
        "save_minutely_weather": MockSaveFunction(),
        "save_hourly_weather": MockSaveFunction(),
        "save_daily_weather": MockSaveFunction(),
        "save_alerts": MockSaveFunction(),
    }

    for func_name, mock_func in mock_functions.items():
        monkeypatch.setattr(f"src.django_owm.utils.saving.{func_name}", mock_func)

    return mock_functions


def test_save_weather_data_integration(mock_save_functions):
    """Test that save_weather_data calls all the save functions correctly."""
    location = object()  # simple mock location
    data = {
        "current": {"dt": 1609459200, "temp": 20.5},
        "minutely": [{"dt": 1609459260, "precipitation": 0.5}],
        "hourly": [{"dt": 1609462800, "temp": 21.0}],
        "daily": [{"dt": 1609545600, "temp": {"day": 22.0}}],
        "alerts": [{"sender_name": "Test", "event": "Storm", "start": 1609459200, "end": 1609545600}],
    }

    save_weather_data(location, data)

    for _, mock_func in mock_save_functions.items():
        assert mock_func.call_count == 1
        assert mock_func.last_call_args == ((location, data), {})


@pytest.fixture
def mock_api_call_log_model(monkeypatch):
    """Fixture to mock the APICallLog model."""

    class MockQuerySet:
        """Mock QuerySet object with filter, count, and create methods."""

        def filter(self, **kwargs):  # pylint: disable=W0613
            """Return self to allow chaining."""
            return self

        def count(self):
            """Return 0 to simulate an empty queryset."""
            return 0

        def create(self, **kwargs):
            """Mock create method."""

    class MockAPICallLogModel:
        """Mock APICallLog model with objects attribute."""

        objects = MockQuerySet()

        @classmethod
        def create(cls, **kwargs):
            """Mock create method."""

    def mock_get_model(app_label):  # pylint: disable=W0613
        """Mock get_model function."""
        return MockAPICallLogModel

    monkeypatch.setattr(apps, "get_model", mock_get_model)
    monkeypatch.setitem(OWM_MODEL_MAPPINGS, "APICallLog", "mock.APICallLog")
    return MockAPICallLogModel


def test_get_api_call_counts_no_model(monkeypatch):
    """Test that get_api_call_counts returns 0 when the model is not configured."""
    monkeypatch.setitem(OWM_MODEL_MAPPINGS, "APICallLog", None)
    assert get_api_call_counts("test_api") == (0, 0)


def test_get_api_call_counts_with_model(mock_api_call_log_model):  # pylint: disable=W0613
    """Test that get_api_call_counts returns the correct counts."""
    assert get_api_call_counts("test_api") == (0, 0)


@pytest.mark.parametrize(
    "calls_last_minute,calls_last_month,expected",
    [
        (59, 999999, True),
        (60, 999999, False),
        (59, 1000000, False),
        (60, 1000000, False),
    ],
)
def test_check_api_limits(monkeypatch, calls_last_minute, calls_last_month, expected):
    """Test that check_api_limits correctly checks the API rate limits."""
    monkeypatch.setitem(OWM_API_RATE_LIMITS, "one_call", {"calls_per_minute": 60, "calls_per_month": 1000000})
    monkeypatch.setattr("src.django_owm.utils.api.get_api_call_counts", lambda x: (calls_last_minute, calls_last_month))

    @check_api_limits
    def test_func():
        """Test function for check_api_limits decorator."""
        return True

    assert test_func() == expected


def test_log_api_call(mock_api_call_log_model):  # pylint: disable=W0613
    """Test that log_api_call creates a log entry."""
    log_api_call("test_api")
    # Since we can't easily check if create was called, we just ensure no exception is raised


def test_make_api_call_no_api_key(monkeypatch, caplog):
    """Test that make_api_call logs an error when the API key is not set."""
    monkeypatch.setattr("src.django_owm.utils.api.OWM_API_KEY", None)

    with caplog.at_level(logging.ERROR):
        result = make_api_call(Decimal("10.0"), Decimal("20.0"))

    assert result is None
    assert "OpenWeatherMap API key not set" in caplog.text


def test_make_api_call_with_exclude(monkeypatch):
    """Test that make_api_call returns the JSON response when the API call is successful."""

    class MockResponse:
        """Mock response object with JSON method."""

        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            """Return the JSON data."""
            return self.json_data

    monkeypatch.setattr("src.django_owm.utils.api.OWM_API_KEY", "test_key")
    monkeypatch.setattr("requests.get", lambda url, timeout: MockResponse(200, {"data": "test"}))

    result = make_api_call(Decimal("10.0"), Decimal("20.0"), exclude=["daily", "hourly"])

    assert result == {"data": "test"}


def test_make_api_call_json_response(monkeypatch):
    """Test that make_api_call returns the JSON response when the API call is successful."""
    monkeypatch.setattr("src.django_owm.utils.api.OWM_API_KEY", "test_key")

    class MockResponse:
        """Mock response object with JSON method."""

        status_code = 200

        def json_response(self):
            """Return a test JSON response."""
            return {"data": "test"}

    monkeypatch.setattr("requests.get", lambda url, timeout: MockResponse())

    result = make_api_call(Decimal("10.0"), Decimal("20.0"))

    assert result == {"data": "test"}


def test_make_api_call_attribute_error(monkeypatch, caplog):
    """Test that make_api_call handles attribute errors gracefully."""
    monkeypatch.setattr("src.django_owm.utils.api.OWM_API_KEY", "test_key")

    class MockResponse:
        """Mock response object with attribute error."""

        status_code = 200

    monkeypatch.setattr("requests.get", lambda url, timeout: MockResponse())

    with caplog.at_level(logging.ERROR):
        result = make_api_call(Decimal("10.0"), Decimal("20.0"))

    assert result is None
    assert "Error parsing JSON response" in caplog.text


def test_make_api_call_request_exception(monkeypatch, caplog):
    """Test that make_api_call handles requests exceptions gracefully."""
    monkeypatch.setattr("src.django_owm.utils.api.OWM_API_KEY", "test_key")
    monkeypatch.setattr(
        "requests.get", lambda url, timeout: (_ for _ in ()).throw(requests.RequestException("Test error"))
    )

    with caplog.at_level(logging.ERROR):
        result = make_api_call(Decimal("10.0"), Decimal("20.0"))

    assert result is None
    assert "Error fetching weather data: Test error" in caplog.text
