"""Models for testing the django_owm app."""

from src.django_owm.models import AbstractAPICallLog
from src.django_owm.models import AbstractCurrentWeather
from src.django_owm.models import AbstractDailyWeather
from src.django_owm.models import AbstractHourlyWeather
from src.django_owm.models import AbstractMinutelyWeather
from src.django_owm.models import AbstractWeatherAlert
from src.django_owm.models import AbstractWeatherErrorLog
from src.django_owm.models import AbstractWeatherLocation


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
