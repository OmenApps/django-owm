"""Models for testing the django_owm app."""

from src.django_owm.models import APICallLog as AbstractAPICallLog
from src.django_owm.models import CurrentWeather as AbstractCurrentWeather
from src.django_owm.models import DailyWeather as AbstractDailyWeather
from src.django_owm.models import HourlyWeather as AbstractHourlyWeather
from src.django_owm.models import MinutelyWeather as AbstractMinutelyWeather
from src.django_owm.models import WeatherAlert as AbstractWeatherAlert
from src.django_owm.models import WeatherErrorLog as AbstractWeatherErrorLog
from src.django_owm.models import WeatherLocation as AbstractWeatherLocation


class WeatherLocation(AbstractWeatherLocation):  # pylint: disable=R0903
    """Concrete model for WeatherLocation."""


class CurrentWeather(AbstractCurrentWeather):  # pylint: disable=R0903
    """Concrete model for CurrentWeather."""


class MinutelyWeather(AbstractMinutelyWeather):  # pylint: disable=R0903
    """Concrete model for MinutelyWeather."""


class HourlyWeather(AbstractHourlyWeather):  # pylint: disable=R0903
    """Concrete model for HourlyWeather."""


class DailyWeather(AbstractDailyWeather):  # pylint: disable=R0903
    """Concrete model for DailyWeather."""


class WeatherAlert(AbstractWeatherAlert):  # pylint: disable=R0903
    """Concrete model for WeatherAlert."""


class WeatherErrorLog(AbstractWeatherErrorLog):  # pylint: disable=R0903
    """Concrete model for WeatherErrorLog."""


class APICallLog(AbstractAPICallLog):  # pylint: disable=R0903
    """Concrete model for APICallLog."""
