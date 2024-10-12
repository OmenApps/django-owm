"""Base Models for django_owm. These are not meant to be used directly."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..app_settings import OWM_BASE_MODEL
from ..app_settings import OWM_MODEL_MAPPINGS


if callable(OWM_BASE_MODEL):
    OWM_BASE_MODEL = OWM_BASE_MODEL()


class AbstractBaseWeatherData(OWM_BASE_MODEL):
    """Abstract base model for storing weather data. Not intended to be used directly."""

    location = models.ForeignKey(
        OWM_MODEL_MAPPINGS["WeatherLocation"],
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_weather_data",
        related_query_name="%(app_label)s_%(class)ss",
        help_text=_("Location for this weather data"),
    )
    timestamp = models.DateTimeField(
        _("Timestamp"),
        help_text=_("Unix timestamp converted to DateTime"),
    )
    pressure = models.IntegerField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    dew_point = models.DecimalField(
        _("Dew Point"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    uvi = models.DecimalField(
        _("UV Index"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    clouds = models.IntegerField(blank=True, null=True)
    wind_speed = models.DecimalField(
        _("Wind Speed"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wind_deg = models.IntegerField(blank=True, null=True)
    wind_gust = models.DecimalField(
        _("Wind Gust"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weather_condition_id = models.IntegerField()
    weather_condition_main = models.CharField(max_length=255)
    weather_condition_description = models.CharField(max_length=255, help_text=_("Icon description"))
    weather_condition_icon = models.CharField(max_length=10)

    class Meta(OWM_BASE_MODEL.Meta):
        """Meta options for the WeatherData model."""

        abstract = True

    @property
    def icon_url(self):
        """Return the URL for the weather condition icon."""
        return f"https://openweathermap.org/img/wn/{self.weather_condition_icon}.png"

    @property
    def large_icon_url(self):
        """Return the URL for the weather condition icon."""
        return f"https://openweathermap.org/img/wn/{self.weather_condition_icon}@2x.png"

    @property
    def weather_description(self):
        """Return the weather description.

        https://openweathermap.org/weather-conditions
        """
        weather_description_mapping = {
            200: "thunderstorm with light rain",
            201: "thunderstorm with rain",
            202: "thunderstorm with heavy rain",
            210: "light thunderstorm",
            211: "thunderstorm",
            212: "heavy thunderstorm",
            221: "ragged thunderstorm",
            230: "thunderstorm with light drizzle",
            231: "thunderstorm with drizzle",
            232: "thunderstorm with heavy drizzle",
            300: "light intensity drizzle",
            301: "drizzle",
            302: "heavy intensity drizzle",
            310: "light intensity drizzle rain",
            311: "drizzle rain",
            312: "heavy intensity drizzle rain",
            313: "shower rain and drizzle",
            314: "heavy shower rain and drizzle",
            321: "shower drizzle",
            500: "light rain",
            501: "moderate rain",
            502: "heavy intensity rain",
            503: "very heavy rain",
            504: "extreme rain",
            511: "freezing rain",
            520: "light intensity shower rain",
            521: "shower rain",
            522: "heavy intensity shower rain",
            531: "ragged shower rain",
            600: "light snow",
            601: "snow",
            602: "heavy snow",
            611: "sleet",
            612: "light shower sleet",
            613: "shower sleet",
            615: "light rain and snow",
            616: "rain and snow",
            620: "light shower snow",
            621: "shower snow",
            622: "heavy shower snow",
            701: "mist",
            711: "smoke",
            721: "haze",
            731: "sand/dust whirls",
            741: "fog",
            751: "sand",
            761: "dust",
            762: "volcanic ash",
            771: "squalls",
            781: "tornado",
            800: "clear sky",
            801: "few clouds: 11-25%",
            802: "scattered clouds: 25-50%",
            803: "broken clouds: 51-84%",
            804: "overcast clouds: 85-100%",
        }
        return weather_description_mapping.get(self.weather_condition_id, self.weather_condition_description)
