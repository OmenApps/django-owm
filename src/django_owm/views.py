"""Views for the django_owm app."""

from django.apps import apps
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .app_settings import OWM_MODEL_MAPPINGS


def weather_detail(request, location_id):
    """View to display the weather details for a location."""
    model_mappings = OWM_MODEL_MAPPINGS
    WeatherLocationModel = apps.get_model(model_mappings.get("WeatherLocation"))  # pylint: disable=C0103
    CurrentWeatherModel = apps.get_model(model_mappings.get("CurrentWeather"))  # pylint: disable=C0103

    location = get_object_or_404(WeatherLocationModel, pk=location_id)
    current_weather = CurrentWeatherModel.objects.filter(location=location).order_by("-timestamp").first()

    context = {
        "location": location,
        "current_weather": current_weather,
    }

    return render(request, "django_owm/weather_detail.html", context)
