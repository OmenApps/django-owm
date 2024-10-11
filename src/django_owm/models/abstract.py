"""Models for OpenWeatherMap API data storage in django_owm."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..app_settings import OWM_BASE_MODEL
from ..app_settings import OWM_MODEL_MAPPINGS
from .base import AbstractBaseWeatherData


class WeatherLocation(OWM_BASE_MODEL):  # pylint: disable=R0903
    """Abstract model for storing weather location data."""

    name = models.CharField(
        _("Location Name"),
        max_length=255,
        blank=True,
        null=True,
    )
    latitude = models.DecimalField(
        _("Latitude"),
        max_digits=5,
        decimal_places=2,
        help_text=_("Latitude of the location, decimal (−90; 90)"),
    )
    longitude = models.DecimalField(
        _("Longitude"),
        max_digits=5,
        decimal_places=2,
        help_text=_("Longitude of the location, decimal (−180; 180)"),
    )
    timezone = models.CharField(
        _("Timezone"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Timezone name for the requested location"),
    )
    timezone_offset = models.IntegerField(
        _("Timezone Offset"),
        blank=True,
        null=True,
        help_text=_("Offset from UTC in seconds"),
    )

    class Meta(OWM_BASE_MODEL.Meta):  # pylint: disable=R0903
        """Meta options for the WeatherLocation model."""

        abstract = True


class CurrentWeather(AbstractBaseWeatherData):  # pylint: disable=R0903
    """Abstract model for storing current weather data."""

    sunrise = models.DateTimeField(blank=True, null=True)
    sunset = models.DateTimeField(blank=True, null=True)
    temp = models.DecimalField(
        _("Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    feels_like = models.DecimalField(
        _("Feels Like Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    visibility = models.IntegerField(blank=True, null=True)
    rain_1h = models.DecimalField(
        _("Rain (1h)"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Precipitation in mm/h"),
    )
    snow_1h = models.DecimalField(
        _("Snow (1h)"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Snowfall in mm/h"),
    )

    class Meta:  # pylint: disable=R0903
        """Meta options for the CurrentWeather model."""

        abstract = True


class MinutelyWeather(OWM_BASE_MODEL):  # pylint: disable=R0903
    """Abstract model for storing minutely weather data."""

    location = models.ForeignKey(
        OWM_MODEL_MAPPINGS["WeatherLocation"],
        on_delete=models.CASCADE,
        related_name="minutely_weather",
        help_text=_("Location for this weather data by minute"),
    )
    timestamp = models.DateTimeField(
        _("Timestamp"),
        help_text=_("Unix timestamp converted to DateTime"),
    )
    precipitation = models.DecimalField(
        _("Precipitation"),
        max_digits=5,
        decimal_places=2,
    )

    class Meta(OWM_BASE_MODEL.Meta):  # pylint: disable=R0903
        """Meta options for the MinutelyWeather model."""

        abstract = True


class HourlyWeather(AbstractBaseWeatherData):  # pylint: disable=R0903
    """Abstract model for storing hourly weather data."""

    temp = models.DecimalField(
        _("Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    feels_like = models.DecimalField(
        _("Feels Like Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    visibility = models.IntegerField(blank=True, null=True)
    pop = models.DecimalField(
        _("Probability of Precipitation"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    rain_1h = models.DecimalField(
        _("Rain (1h)"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    snow_1h = models.DecimalField(
        _("Snow (1h)"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:  # pylint: disable=R0903
        """Meta options for the HourlyWeather model."""

        abstract = True


class DailyWeather(AbstractBaseWeatherData):  # pylint: disable=R0903
    """Abstract model for storing daily weather data."""

    sunrise = models.DateTimeField(blank=True, null=True)
    sunset = models.DateTimeField(blank=True, null=True)
    moonrise = models.DateTimeField(blank=True, null=True)
    moonset = models.DateTimeField(blank=True, null=True)
    moon_phase = models.DecimalField(
        _("Moon Phase"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    summary = models.TextField(blank=True, null=True)
    temp_min = models.DecimalField(
        _("Temperature Min"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    temp_max = models.DecimalField(
        _("Temperature Max"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    temp_morn = models.DecimalField(
        _("Morning Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    temp_day = models.DecimalField(
        _("Day Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    temp_eve = models.DecimalField(
        _("Evening Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    temp_night = models.DecimalField(
        _("Night Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    feels_like_morn = models.DecimalField(
        _("Feels Like - Morning"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    feels_like_day = models.DecimalField(
        _("Feels Like - Day"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    feels_like_eve = models.DecimalField(
        _("Feels Like - Evening"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    feels_like_night = models.DecimalField(
        _("Feels Like - Night"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pop = models.DecimalField(
        _("Probability of Precipitation"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    rain = models.DecimalField(
        _("Rain"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    snow = models.DecimalField(
        _("Snow"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:  # pylint: disable=R0903
        """Meta options for the DailyWeather model."""

        abstract = True

    @property
    def moon_phase_description(self):  # pylint: disable=R0911
        """Return a description of the moon phase."""

        match self.moon_phase:
            case 0 | 1:
                return _("New Moon")
            case 0.25:
                return _("First Quarter")
            case 0.5:
                return _("Full Moon")
            case 0.75:
                return _("Last Quarter")
            case phase if 0 < phase < 0.25:
                return _("Waxing Crescent")
            case phase if 0.25 < phase < 0.5:
                return _("Waxing Gibbous")
            case phase if 0.5 < phase < 0.75:
                return _("Waning Gibbous")
            case phase if 0.75 < phase < 1:
                return _("Waning Crescent")
            case _:
                return _("Unknown")


class WeatherAlert(OWM_BASE_MODEL):  # pylint: disable=R0903
    """Abstract model for storing weather alerts."""

    location = models.ForeignKey(
        OWM_MODEL_MAPPINGS["WeatherLocation"],
        on_delete=models.CASCADE,
        related_name="weather_alerts",
    )
    sender_name = models.CharField(max_length=255)
    event = models.CharField(max_length=255)
    start = models.DateTimeField(_("Start Time"), help_text=_("Start time of the alert"))
    end = models.DateTimeField(_("End Time"), help_text=_("End time of the alert"))
    description = models.TextField()
    tags = models.JSONField(default=list, blank=True, null=True)

    class Meta(OWM_BASE_MODEL.Meta):  # pylint: disable=R0903
        """Meta options for the WeatherAlert model."""

        abstract = True


class WeatherErrorLog(OWM_BASE_MODEL):  # pylint: disable=R0903
    """Abstract model for storing weather API error logs."""

    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(
        OWM_MODEL_MAPPINGS["WeatherLocation"],
        on_delete=models.CASCADE,
        related_name="error_logs",
    )
    api_name = models.CharField(max_length=255)
    error_message = models.TextField()
    response_data = models.TextField(blank=True, null=True)

    class Meta(OWM_BASE_MODEL.Meta):  # pylint: disable=R0903
        """Meta options for the WeatherErrorLog model."""

        abstract = True


class APICallLog(OWM_BASE_MODEL):  # pylint: disable=R0903
    """Abstract model for storing API call logs."""

    timestamp = models.DateTimeField(auto_now_add=True)
    api_name = models.CharField(max_length=255)

    class UnitsType(models.TextChoices):
        """Choices for the units type field."""

        STANDARD = "standard", _("Standard")
        METRIC = "metric", _("Metric")
        IMPERIAL = "imperial", _("Imperial")

    units = models.CharField(
        _("Units"),
        max_length=10,
        choices=UnitsType.choices,
        default=UnitsType.STANDARD,
    )

    class Meta(OWM_BASE_MODEL.Meta):  # pylint: disable=R0903
        """Meta options for the APICallLog model."""

        abstract = True
