"""Admin for the django_owm app."""

from django.contrib import admin

from .app_settings import OWM_MODEL_MAPPINGS
from .app_settings import OWM_USE_BUILTIN_ADMIN
from .app_settings import get_model_from_string


if OWM_USE_BUILTIN_ADMIN:
    WeatherLocationModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    WeatherDataModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherData"))
    CurrentWeatherModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("CurrentWeather"))
    WeatherErrorLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))
    APICallLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("APICallLog"))

    if WeatherLocationModel:

        @admin.register(WeatherLocationModel)
        class WeatherLocationAdmin(admin.ModelAdmin):
            """Admin for WeatherLocation model."""
            list_display = ("name", "latitude", "longitude", "timezone")

    if WeatherDataModel:

        @admin.register(WeatherDataModel)
        class WeatherDataAdmin(admin.ModelAdmin):
            """Admin for WeatherData model."""
            list_display = ("location", "timestamp", "temp", "feels_like", "pressure", "humidity")

    if CurrentWeatherModel:

        @admin.register(CurrentWeatherModel)
        class CurrentWeatherAdmin(admin.ModelAdmin):
            """Admin for CurrentWeather model."""
            list_display = ("location", "timestamp", "temp", "feels_like", "pressure", "humidity")

    if WeatherErrorLogModel:

        @admin.register(WeatherErrorLogModel)
        class WeatherErrorLogAdmin(admin.ModelAdmin):
            """Admin for WeatherErrorLog model."""
            list_display = ("timestamp", "location", "api_name", "error_message")

    if APICallLogModel:

        @admin.register(APICallLogModel)
        class APICallLogAdmin(admin.ModelAdmin):
            """Admin for APICallLog model."""
            list_display = ("timestamp", "api_name")
