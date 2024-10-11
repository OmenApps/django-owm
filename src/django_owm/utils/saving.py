"""Utility functions for saving weather data to the database."""

from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Optional

from django.utils import timezone

from ..app_settings import OWM_MODEL_MAPPINGS
from ..app_settings import get_model_from_string


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..models import WeatherLocation


def save_weather_data(location: WeatherLocation, data: Dict[str, Any]):
    """Save weather data to the database."""
    if data:
        save_current_weather(location, data)
        save_minutely_weather(location, data)
        save_hourly_weather(location, data)
        save_daily_weather(location, data)
        save_alerts(location, data)


def save_current_weather(location: WeatherLocation, data: Dict[str, Any]):
    """Save current weather data to the database."""
    model_mappings = OWM_MODEL_MAPPINGS
    CurrentWeatherModel = get_model_from_string(model_mappings.get("CurrentWeather"))  # pylint: disable=C0103

    if not CurrentWeatherModel:
        logger.error("CurrentWeatherModel is not configured.")
        return

    current_data = data.get("current", {})
    if not current_data:
        return

    timestamp = timezone.datetime.fromtimestamp(current_data["dt"], tz=datetime.timezone.utc)
    weather_condition = current_data.get("weather", None)
    weather_condition = weather_condition[0] if weather_condition else {}
    CurrentWeatherModel.objects.create(
        location=location,
        timestamp=timestamp,
        temp=current_data.get("temp"),
        feels_like=current_data.get("feels_like"),
        pressure=current_data.get("pressure"),
        humidity=current_data.get("humidity"),
        dew_point=current_data.get("dew_point"),
        uvi=current_data.get("uvi"),
        clouds=current_data.get("clouds"),
        visibility=current_data.get("visibility"),
        wind_speed=current_data.get("wind_speed"),
        wind_deg=current_data.get("wind_deg"),
        wind_gust=current_data.get("wind_gust"),
        rain_1h=current_data.get("rain", {}).get("1h"),
        snow_1h=current_data.get("snow", {}).get("1h"),
        weather_condition_id=weather_condition.get("id"),
        weather_condition_main=weather_condition.get("main"),
        weather_condition_description=weather_condition.get("description"),
        weather_condition_icon=weather_condition.get("icon"),
    )


def save_minutely_weather(location: WeatherLocation, data: Dict[str, Any]):
    """Save minutely weather data to the database."""
    model_mappings = OWM_MODEL_MAPPINGS
    MinutelyWeatherModel = get_model_from_string(model_mappings.get("MinutelyWeather"))  # pylint: disable=C0103

    if not MinutelyWeatherModel:
        logger.error("MinutelyWeatherModel is not configured.")
        return

    minutely_data = data.get("minutely", [])
    if not minutely_data:
        return

    for minute_data in minutely_data:
        timestamp = timezone.datetime.fromtimestamp(minute_data["dt"], tz=datetime.timezone.utc)
        MinutelyWeatherModel.objects.create(
            location=location,
            timestamp=timestamp,
            precipitation=minute_data.get("precipitation"),
        )


def save_hourly_weather(location: WeatherLocation, data: Dict[str, Any]):
    """Save hourly weather data to the database."""
    model_mappings = OWM_MODEL_MAPPINGS
    HourlyWeatherModel = get_model_from_string(model_mappings.get("HourlyWeather"))  # pylint: disable=C0103

    if not HourlyWeatherModel:
        logger.error("HourlyWeatherModel is not configured.")
        return

    hourly_data = data.get("hourly", [])
    if not hourly_data:
        return

    for hour_data in hourly_data:
        timestamp = timezone.datetime.fromtimestamp(hour_data["dt"], tz=datetime.timezone.utc)
        weather_condition = hour_data.get("weather", None)
        weather_condition = weather_condition[0] if weather_condition else {}
        HourlyWeatherModel.objects.create(
            location=location,
            timestamp=timestamp,
            temp=hour_data.get("temp"),
            feels_like=hour_data.get("feels_like"),
            pressure=hour_data.get("pressure"),
            humidity=hour_data.get("humidity"),
            dew_point=hour_data.get("dew_point"),
            uvi=hour_data.get("uvi"),
            clouds=hour_data.get("clouds"),
            visibility=hour_data.get("visibility"),
            wind_speed=hour_data.get("wind_speed"),
            wind_deg=hour_data.get("wind_deg"),
            wind_gust=hour_data.get("wind_gust"),
            rain_1h=hour_data.get("rain", {}).get("1h"),
            snow_1h=hour_data.get("snow", {}).get("1h"),
            weather_condition_id=weather_condition.get("id"),
            weather_condition_main=weather_condition.get("main"),
            weather_condition_description=weather_condition.get("description"),
            weather_condition_icon=weather_condition.get("icon"),
        )


def save_daily_weather(location: WeatherLocation, data: Dict[str, Any]):
    """Save daily weather data to the database."""
    model_mappings = OWM_MODEL_MAPPINGS
    DailyWeatherModel = get_model_from_string(model_mappings.get("DailyWeather"))  # pylint: disable=C0103

    if not DailyWeatherModel:
        logger.error("DailyWeatherModel is not configured.")
        return

    daily_data = data.get("daily", [])
    if not daily_data:
        return

    for day_data in daily_data:
        timestamp = timezone.datetime.fromtimestamp(day_data["dt"], tz=datetime.timezone.utc)
        weather_condition = day_data.get("weather", None)
        weather_condition = weather_condition[0] if weather_condition else {}
        DailyWeatherModel.objects.create(
            location=location,
            timestamp=timestamp,
            sunrise=timezone.datetime.fromtimestamp(day_data["sunrise"], tz=datetime.timezone.utc),
            sunset=timezone.datetime.fromtimestamp(day_data["sunset"], tz=datetime.timezone.utc),
            temp_day=day_data.get("temp", {}).get("day"),
            temp_min=day_data.get("temp", {}).get("min"),
            temp_max=day_data.get("temp", {}).get("max"),
            temp_night=day_data.get("temp", {}).get("night"),
            temp_eve=day_data.get("temp", {}).get("eve"),
            temp_morn=day_data.get("temp", {}).get("morn"),
            feels_like_day=day_data.get("feels_like", {}).get("day"),
            feels_like_night=day_data.get("feels_like", {}).get("night"),
            feels_like_eve=day_data.get("feels_like", {}).get("eve"),
            feels_like_morn=day_data.get("feels_like", {}).get("morn"),
            pressure=day_data.get("pressure"),
            humidity=day_data.get("humidity"),
            dew_point=day_data.get("dew_point"),
            uvi=day_data.get("uvi"),
            clouds=day_data.get("clouds"),
            wind_speed=day_data.get("wind_speed"),
            wind_deg=day_data.get("wind_deg"),
            wind_gust=day_data.get("wind_gust"),
            rain=day_data.get("rain"),
            snow=day_data.get("snow"),
            weather_condition_id=weather_condition.get("id"),
            weather_condition_main=weather_condition.get("main"),
            weather_condition_description=weather_condition.get("description"),
            weather_condition_icon=weather_condition.get("icon"),
        )


def save_alerts(location: WeatherLocation, data: Dict[str, Any]):
    """Save weather alerts to the database."""
    model_mappings = OWM_MODEL_MAPPINGS
    WeatherAlertModel = get_model_from_string(model_mappings.get("WeatherAlert"))  # pylint: disable=C0103

    if not WeatherAlertModel:
        logger.error("WeatherAlertModel is not configured.")
        return

    alerts = data.get("alerts", [])
    if not alerts:
        return

    for alert in alerts:
        start = timezone.datetime.fromtimestamp(alert["start"], tz=datetime.timezone.utc)
        end = timezone.datetime.fromtimestamp(alert["end"], tz=datetime.timezone.utc)
        WeatherAlertModel.objects.create(
            location=location,
            sender_name=alert.get("sender_name"),
            event=alert.get("event"),
            start=start,
            end=end,
            description=alert.get("description"),
        )


def save_error_log(
    location: WeatherLocation,
    api_name: str,
    error_message: str,
    response_data: Optional[Dict[str, Any]] = None,
):
    """Save error log to the database."""
    WeatherErrorLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))  # pylint: disable=C0103
    if not WeatherErrorLogModel:
        logger.error("WeatherErrorLogModel is not configured.")
        return
    WeatherErrorLogModel.objects.create(
        location=location,
        api_name=api_name,
        error_message=error_message,
        response_data=response_data,
    )
