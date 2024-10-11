"""Optional concrete models for django_owm app."""

from ..app_settings import OWM_USE_BUILTIN_CONCRETE_MODELS
from .abstract import AbstractAPICallLog
from .abstract import AbstractCurrentWeather
from .abstract import AbstractDailyWeather
from .abstract import AbstractHourlyWeather
from .abstract import AbstractMinutelyWeather
from .abstract import AbstractWeatherAlert
from .abstract import AbstractWeatherErrorLog
from .abstract import AbstractWeatherLocation


if OWM_USE_BUILTIN_CONCRETE_MODELS:
    # Create concrete models for each of the abstract models

    class WeatherLocation(AbstractWeatherLocation):
        """Concrete model for WeatherLocation."""

    class CurrentWeather(AbstractCurrentWeather):
        """Concrete model for AbstractCurrentWeather."""

    class MinutelyWeather(AbstractMinutelyWeather):
        """Concrete model for AbstractMinutelyWeather."""

    class HourlyWeather(AbstractHourlyWeather):
        """Concrete model for AbstractHourlyWeather."""

    class DailyWeather(AbstractDailyWeather):
        """Concrete model for AbstractDailyWeather."""

    class WeatherAlert(AbstractWeatherAlert):
        """Concrete model for AbstractWeatherAlert."""

    class WeatherErrorLog(AbstractWeatherErrorLog):
        """Concrete model for AbstractWeatherErrorLog."""

    class APICallLog(AbstractAPICallLog):
        """Concrete model for AbstractAPICallLog."""
