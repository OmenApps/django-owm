"""Utility functions for working with the OpenWeatherMap API."""

import logging
from collections.abc import Callable
from decimal import Decimal
from functools import wraps

import requests
from django.apps import apps
from django.utils import timezone

from ..app_settings import OWM_API_KEY
from ..app_settings import OWM_API_RATE_LIMITS
from ..app_settings import OWM_MODEL_MAPPINGS


logger = logging.getLogger(__name__)


def get_api_call_counts(api_name: str) -> tuple[int, int]:
    """Get the number of API calls made in the last minute and last month."""
    now = timezone.now()
    one_minute_ago = now - timezone.timedelta(minutes=1)
    one_month_ago = now - timezone.timedelta(days=30)
    model_string = OWM_MODEL_MAPPINGS.get("APICallLog")
    APICallLog = apps.get_model(model_string) if model_string else None
    if not APICallLog:
        return 0, 0
    calls_last_minute = APICallLog.objects.filter(api_name=api_name, timestamp__gte=one_minute_ago).count()
    calls_last_month = APICallLog.objects.filter(api_name=api_name, timestamp__gte=one_month_ago).count()
    return calls_last_minute, calls_last_month


def check_api_limits(func: Callable) -> Callable:
    """Decorator to check API call limits before running a task."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> bool | Callable:
        """Check API call limits before running the task."""
        api_name = "one_call"
        rate_limits = OWM_API_RATE_LIMITS.get(api_name, {})
        calls_per_minute = rate_limits.get("calls_per_minute", 60)
        calls_per_month = rate_limits.get("calls_per_month", 1000000)

        calls_last_minute, calls_last_month = get_api_call_counts(api_name)
        if calls_last_minute >= calls_per_minute or calls_last_month >= calls_per_month:
            logger.warning("API call limit exceeded. Skipping task.")
            return False

        return func(*args, **kwargs)

    return wrapper


def log_api_call(api_name: str) -> None:
    """Log an API call to the database."""
    model_string = OWM_MODEL_MAPPINGS.get("APICallLog")
    APICallLog = apps.get_model(model_string) if model_string else None
    if APICallLog:
        APICallLog.objects.create(api_name=api_name)


def make_api_call(lat: Decimal, lon: Decimal, exclude: list[str] | None = None) -> dict | None:
    """Make an API call to OpenWeatherMap."""
    api_key = OWM_API_KEY
    if not api_key:
        logger.error("OpenWeatherMap API key not set. Please set OWM_API_KEY in your settings.")
        return None

    exclude = ""
    if exclude is not None:
        exclude = ",".join(exclude)

    url = "https://api.openweathermap.org/data/3.0/onecall?" f"lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if hasattr(response, "json"):
                data = response.json()
            elif hasattr(response, "json_response"):
                data = response.json_response()
            else:
                logger.error("Error parsing JSON response.")
                return None

            # Convert relevant float values to Decimal
            current = data.get("current", {})
            for key in ["temp", "feels_like", "dew_point", "uvi", "wind_speed", "wind_gust"]:
                if key in current:
                    current[key] = str(current[key])
            return data
        logger.error("Error fetching weather data: %s", response.text)
        return None
    except requests.RequestException as e:
        logger.exception("Error fetching weather data: %s", e)
        return None
