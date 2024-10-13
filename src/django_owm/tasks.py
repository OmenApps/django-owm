"""Celery tasks for fetching weather data from OpenWeatherMap API for django_owm."""

import logging
from decimal import Decimal

from celery import shared_task
from django.apps import apps

from .app_settings import OWM_API_RATE_LIMITS
from .app_settings import OWM_MODEL_MAPPINGS
from .utils.api import check_api_limits
from .utils.api import get_api_call_counts
from .utils.api import log_api_call
from .utils.api import make_api_call
from .utils.saving import save_error_log
from .utils.saving import save_weather_data


logger = logging.getLogger(__name__)


@shared_task
@check_api_limits
def fetch_weather(location_ids: Decimal | int | None = None) -> None:
    """Fetch current weather data for all locations."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))

    if location_ids is not None:
        locations = WeatherLocationModel.objects.filter(id__in=location_ids)
    else:
        locations = WeatherLocationModel.objects.all()

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
