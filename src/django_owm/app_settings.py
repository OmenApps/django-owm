"""App settings for the django_owm app."""

from django.conf import settings
from django.db import models


DJANGO_OWM = getattr(settings, "DJANGO_OWM", {})

# Example:
# DJANGO_OWM = {
#     'OWM_API_KEY': None,  # Developer should provide their API key in settings.py
#     'OWM_API_RATE_LIMITS': {
#         'one_call': {
#             'calls_per_minute': 60,
#             'calls_per_month': 1000000,
#         },
#         # Future APIs will be added here
#     },
#     'OWM_MODEL_MAPPINGS': {  # Maps abstract model names to appname.ModelName
#         'WeatherLocation': 'myapp.MyWeatherLocation',
#         'CurrentWeather': 'myapp.MyCurrentWeather',
#         'MinutelyWeather': 'myapp.MyMinutelyWeather',
#         'HourlyWeather': 'myapp.MyHourlyWeather',
#         'DailyWeather': 'myapp.MyDailyWeather',
#         'WeatherAlert': 'myapp.MyWeatherAlert',
#         'WeatherErrorLog': 'myapp.MyWeatherErrorLog',
#         'APICallLog': 'myapp.MyAPICallLog',
#     },
#     'OWM_BASE_MODEL': models.Model,  # Base model for OWM models
#     'OWM_USE_BUILTIN_ADMIN': True,  # Use built-in admin for OWM models
#     'OWM_USE_BUILTIN_CONCRETE_MODELS': False,  # Use built-in concrete models
#     'OWM_SHOW_MAP': False,  # Show map in admin for AbstractWeatherLocation
#     'OWM_USE_UUID': False,  # Use UUIDs with OWM models
# }


def get_base_model():
    """Get the base model for OWM models."""

    class Model(models.Model):
        """Simply provides a base model with a Meta class."""

        class Meta:
            """Meta options for the base model."""

            abstract = True

        objects = models.Manager()

    return Model


OWM_API_KEY = DJANGO_OWM.get("OWM_API_KEY", None)
OWM_API_RATE_LIMITS = DJANGO_OWM.get(
    "OWM_API_RATE_LIMITS", {"one_call": {"calls_per_minute": 60, "calls_per_month": 1000000}}
)
OWM_MODEL_MAPPINGS = DJANGO_OWM.get("OWM_MODEL_MAPPINGS", {})
OWM_BASE_MODEL = DJANGO_OWM.get("OWM_BASE_MODEL", get_base_model)
OWM_USE_BUILTIN_ADMIN = DJANGO_OWM.get("OWM_USE_BUILTIN_ADMIN", True)
OWM_SHOW_MAP = DJANGO_OWM.get("OWM_SHOW_MAP", False)
OWM_USE_UUID = DJANGO_OWM.get("OWM_USE_UUID", False)

OWM_USE_BUILTIN_CONCRETE_MODELS = DJANGO_OWM.get("OWM_USE_BUILTIN_CONCRETE_MODELS", False)

if OWM_USE_BUILTIN_CONCRETE_MODELS:
    OWM_MODEL_MAPPINGS = {
        "WeatherLocation": "django_owm.WeatherLocation",
        "CurrentWeather": "django_owm.CurrentWeather",
        "MinutelyWeather": "django_owm.MinutelyWeather",
        "HourlyWeather": "django_owm.HourlyWeather",
        "DailyWeather": "django_owm.DailyWeather",
        "WeatherAlert": "django_owm.WeatherAlert",
        "WeatherErrorLog": "django_owm.WeatherErrorLog",
        "APICallLog": "django_owm.APICallLog",
    }
