"""App settings for the django_owm app."""
from django.conf import settings
from django.db import models
from django.apps import apps


DJANGO_OWM = getattr(settings, 'DJANGO_OWM', {})

# Example:
# DJANGO_OWM = {
#     'OWM_API_KEY': '',  # Developer should provide their API key in settings.py
#     'OWM_API_RATE_LIMITS': {
#         'one_call': {
#             'calls_per_minute': 60,
#             'calls_per_month': 1000000,
#         },
#         # Future APIs can be added here
#     },
#     'OWM_MODEL_MAPPINGS': {
#         # Map abstract model names to concrete model paths
#         # 'WeatherLocation': 'myapp.models.MyWeatherLocation',
#         # 'CurrentWeather': 'myapp.models.MyCurrentWeather',
#         # 'WeatherCondition': 'myapp.models.MyWeatherCondition',
#         # etc.
#     },
#     'OWM_BASE_MODEL': models.Model,  # Base model for OWM models
#     'OWM_USE_BUILTIN_ADMIN': True,  # Use built-in admin for OWM models
# }

class Model(models.Model):
    """Simply provides a base model with a Meta class."""
    class Meta:
        abstract = True

    objects = models.Manager()


OWM_API_KEY = DJANGO_OWM.get('OWM_API_KEY', '')
OWM_API_RATE_LIMITS = DJANGO_OWM.get('OWM_API_RATE_LIMITS', {"one_call": {"calls_per_minute": 60, "calls_per_month": 1000000}})
OWM_MODEL_MAPPINGS = DJANGO_OWM.get('OWM_MODEL_MAPPINGS', {})
OWM_BASE_MODEL = DJANGO_OWM.get('OWM_BASE_MODEL', Model)
OWM_USE_BUILTIN_ADMIN = DJANGO_OWM.get('OWM_USE_BUILTIN_ADMIN', True)

def get_model_from_string(model_string):
    """Get a model class from a string like 'app_label.model_name'."""
    app_label, model_name = model_string.split('.')
    return apps.get_model(app_label=app_label, model_name=model_name)
