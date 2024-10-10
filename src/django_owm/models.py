"""Models for OpenWeatherMap API data storage in django_owm."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .app_settings import OWM_BASE_MODEL

class WeatherLocation(OWM_BASE_MODEL):
    """Abstract model for storing weather location data."""
    name = models.CharField(
        _("Location Name"),
        max_length=255,
        blank=True,
        null=True
    )
    latitude = models.DecimalField(
        _("Latitude"),
        max_digits=5,
        decimal_places=2,
        )
    longitude = models.DecimalField(
        _("Longitude"),
        max_digits=5,
        decimal_places=2,
        )
    timezone = models.CharField(
        _("Timezone"),
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta(OWM_BASE_MODEL.Meta):
        abstract = True

class WeatherData(OWM_BASE_MODEL):
    """Abstract model for storing weather data."""
    location = models.ForeignKey('WeatherLocation', on_delete=models.CASCADE, related_name='weather_data', help_text=_("Location for this weather data"))
    timestamp = models.DateTimeField(
        _("Timestamp"),
        help_text=_("Unix timestamp converted to DateTime"),
    )
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
    visibility = models.IntegerField(blank=True, null=True)
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

    class Meta(OWM_BASE_MODEL.Meta):
        abstract = True

class WeatherCondition(OWM_BASE_MODEL):
    """Abstract model for storing weather condition data."""
    weather_data = models.ForeignKey('WeatherData', related_name='weather_conditions', on_delete=models.CASCADE)
    condition_id = models.IntegerField()
    main = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=10)

    class Meta(OWM_BASE_MODEL.Meta):
        abstract = True

class CurrentWeather(WeatherData):
    """Abstract model for storing current weather data."""
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

    class Meta:
        abstract = True

class MinutelyWeather(OWM_BASE_MODEL):
    """Abstract model for storing minutely weather data."""
    location = models.ForeignKey('WeatherLocation', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
        _("Timestamp"),
        help_text=_("Unix timestamp converted to DateTime"),
    )
    precipitation = models.DecimalField(
        _("Precipitation"),
        max_digits=5,
        decimal_places=2,
    )

    class Meta(OWM_BASE_MODEL.Meta):
        abstract = True

class HourlyWeather(WeatherData):
    """Abstract model for storing hourly weather data."""
    pop = models.DecimalField(
        _("Probability of Precipitation"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True,)
    rain_1h = models.DecimalField(
        _("Rain (1h)"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    snow_1h = models.DecimalField(
        _("Snow (1h)"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)

    class Meta:
        abstract = True

class DailyWeather(WeatherData):
    """Abstract model for storing daily weather data."""
    moonrise = models.DateTimeField(blank=True, null=True)
    moonset = models.DateTimeField(blank=True, null=True)
    moon_phase = models.DecimalField(
        _("Moon Phase"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    temp_min = models.DecimalField(
        _("Temperature Min"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    temp_max = models.DecimalField(
        _("Temperature Max"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    temp_morn = models.DecimalField(
        _("Morning Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    temp_day = models.DecimalField(
        _("Day Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    temp_eve = models.DecimalField(
        _("Evening Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    temp_night = models.DecimalField(
        _("Night Temperature"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    feels_like_morn = models.DecimalField(
        _("Feels Like - Morning"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    feels_like_day = models.DecimalField(
        _("Feels Like - Day"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    feels_like_eve = models.DecimalField(
        _("Feels Like - Evening"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    feels_like_night = models.DecimalField(
        _("Feels Like - Night"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    pop = models.DecimalField(
        _("Probability of Precipitation"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    rain = models.DecimalField(
        _("Rain"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)
    snow = models.DecimalField(
        _("Snow"),
        max_digits=5,
        decimal_places=2,
        blank=True, null=True)

    class Meta:
        abstract = True

class WeatherAlert(OWM_BASE_MODEL):
    """Abstract model for storing weather alerts."""
    location = models.ForeignKey('WeatherLocation', on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=255)
    event = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField()
    tags = models.JSONField(blank=True, null=True)

    class Meta(OWM_BASE_MODEL.Meta):
        abstract = True

class WeatherErrorLog(OWM_BASE_MODEL):
    """Abstract model for storing weather API error logs."""
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey('WeatherLocation', on_delete=models.CASCADE)
    api_name = models.CharField(max_length=255)
    error_message = models.TextField()
    response_data = models.TextField(blank=True, null=True)

    class Meta(OWM_BASE_MODEL.Meta):
        abstract = True

class APICallLog(OWM_BASE_MODEL):
    """Abstract model for storing API call logs."""
    timestamp = models.DateTimeField(auto_now_add=True)
    api_name = models.CharField(max_length=255)

    class Meta(OWM_BASE_MODEL.Meta):
        abstract = True
