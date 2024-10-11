"""Admin for the django_owm app."""

from django.apps import apps
from django.contrib import admin

from .app_settings import OWM_MODEL_MAPPINGS
from .app_settings import OWM_USE_BUILTIN_ADMIN


if OWM_USE_BUILTIN_ADMIN:
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    CurrentWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))
    MinutelyWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get("MinutelyWeather"))
    HourlyWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get("HourlyWeather"))
    DailyWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get("DailyWeather"))
    WeatherAlertModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherAlert"))
    WeatherErrorLogModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))
    APICallLogModel = apps.get_model(OWM_MODEL_MAPPINGS.get("APICallLog"))

    if WeatherLocationModel and not admin.site.is_registered(WeatherLocationModel):

        @admin.register(WeatherLocationModel)
        class WeatherLocationAdmin(admin.ModelAdmin):
            """Admin for WeatherLocation model."""

            list_display = ("name", "latitude", "longitude", "timezone")

    if CurrentWeatherModel and not admin.site.is_registered(CurrentWeatherModel):

        @admin.register(CurrentWeatherModel)
        class CurrentWeatherAdmin(admin.ModelAdmin):
            """Admin for CurrentWeather model."""

            list_display = ("location", "timestamp", "temp", "feels_like", "pressure", "humidity")

    if MinutelyWeatherModel and not admin.site.is_registered(MinutelyWeatherModel):

        @admin.register(MinutelyWeatherModel)
        class MinutelyWeatherAdmin(admin.ModelAdmin):
            """Admin for MinutelyWeather model."""

            list_display = ("timestamp", "precipitation")

    if HourlyWeatherModel and not admin.site.is_registered(HourlyWeatherModel):

        @admin.register(HourlyWeatherModel)
        class HourlyWeatherAdmin(admin.ModelAdmin):
            """Admin for HourlyWeather model."""

            list_display = ("timestamp", "temp", "feels_like", "pressure", "humidity")

    if DailyWeatherModel and not admin.site.is_registered(DailyWeatherModel):

        @admin.register(DailyWeatherModel)
        class DailyWeatherAdmin(admin.ModelAdmin):
            """Admin for DailyWeather model."""

            list_display = ("timestamp", "pressure", "humidity")

    if WeatherAlertModel and not admin.site.is_registered(WeatherAlertModel):

        @admin.register(WeatherAlertModel)
        class WeatherAlertAdmin(admin.ModelAdmin):
            """Admin for WeatherAlert model."""

            list_display = ("sender_name", "event", "start", "end")

    if WeatherErrorLogModel and not admin.site.is_registered(WeatherErrorLogModel):

        @admin.register(WeatherErrorLogModel)
        class WeatherErrorLogAdmin(admin.ModelAdmin):
            """Admin for WeatherErrorLog model."""

            list_display = ("timestamp", "location", "api_name", "error_message")

    if APICallLogModel and not admin.site.is_registered(APICallLogModel):

        @admin.register(APICallLogModel)
        class APICallLogAdmin(admin.ModelAdmin):
            """Admin for APICallLog model."""

            list_display = ("timestamp", "api_name")
