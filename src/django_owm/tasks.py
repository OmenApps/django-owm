"""Celery tasks for fetching weather data from OpenWeatherMap API for django_owm."""

import logging

from celery import shared_task

from .app_settings import OWM_API_RATE_LIMITS
from .app_settings import OWM_MODEL_MAPPINGS
from .app_settings import get_model_from_string
from .utils.api import check_api_limits
from .utils.api import get_api_call_counts
from .utils.api import log_api_call
from .utils.api import make_api_call
from .utils.saving import save_error_log
from .utils.saving import save_weather_data


logger = logging.getLogger(__name__)


@shared_task
@check_api_limits
def fetch_weather():
    """Fetch current weather data for all locations."""
    WeatherLocationModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherLocation"))  # pylint: disable=C0103
    if not WeatherLocationModel:
        logger.error("WeatherLocation model is not configured.")
        locations = []
    else:
        locations = WeatherLocationModel.objects.all()
    api_name = "one_call"

    for location in locations:
        calls_last_minute, _ = get_api_call_counts(api_name)
        if calls_last_minute >= OWM_API_RATE_LIMITS.get(api_name, {}).get("calls_per_minute", 60):
            logger.warning("API call limit per minute exceeded. Stopping task.")
            break

        data = make_api_call(location.latitude, location.longitude)
        if data:
            save_weather_data(location, data)
            log_api_call(api_name)
        else:
            error_message = "Failed to fetch weather data"
            save_error_log(location, api_name, error_message)
