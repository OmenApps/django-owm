"""Admin for the django_owm app."""

from django.contrib import admin

from .app_settings import OWM_MODEL_MAPPINGS
from .app_settings import OWM_USE_BUILTIN_ADMIN
from .app_settings import get_model_from_string


if OWM_USE_BUILTIN_ADMIN:
    WeatherLocationModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    CurrentWeatherModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("CurrentWeather"))
    MinutelyWeatherModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("MinutelyWeather"))
    HourlyWeatherModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("HourlyWeather"))
    DailyWeatherModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("DailyWeather"))
    WeatherAlertModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherAlert"))
    WeatherErrorLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))
    APICallLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get("APICallLog"))

    if WeatherLocationModel:

        @admin.register(WeatherLocationModel)
        class WeatherLocationAdmin(admin.ModelAdmin):
            """Admin for WeatherLocation model."""

            list_display = ("name", "latitude", "longitude", "timezone")

    if CurrentWeatherModel:

        @admin.register(CurrentWeatherModel)
        class CurrentWeatherAdmin(admin.ModelAdmin):
            """Admin for CurrentWeather model."""

            list_display = ("location", "timestamp", "temp", "feels_like", "pressure", "humidity")

    if MinutelyWeatherModel:

        @admin.register(MinutelyWeatherModel)
        class MinutelyWeatherAdmin(admin.ModelAdmin):
            """Admin for MinutelyWeather model."""

            list_display = ("timestamp", "precipitation")

    if HourlyWeatherModel:

        @admin.register(HourlyWeatherModel)
        class HourlyWeatherAdmin(admin.ModelAdmin):
            """Admin for HourlyWeather model."""

            list_display = ("timestamp", "temp", "feels_like", "pressure", "humidity")

    if DailyWeatherModel:

        @admin.register(DailyWeatherModel)
        class DailyWeatherAdmin(admin.ModelAdmin):
            """Admin for DailyWeather model."""

            list_display = ("timestamp", "pressure", "humidity")

    if WeatherAlertModel:

        @admin.register(WeatherAlertModel)
        class WeatherAlertAdmin(admin.ModelAdmin):
            """Admin for WeatherAlert model."""

            list_display = ("sender_name", "event", "start", "end")

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
