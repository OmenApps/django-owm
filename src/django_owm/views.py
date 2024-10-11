"""Views for the django_owm app."""

import logging
import uuid
from typing import Union

from django.apps import apps
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from .app_settings import OWM_MODEL_MAPPINGS
from .app_settings import OWM_SHOW_MAP
from .app_settings import OWM_USE_UUID
from .forms import WeatherLocationForm


logger = logging.getLogger(__name__)


def list_locations(request):
    """View to display a list of all weather locations with an optional map."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    locations = WeatherLocationModel.objects.all()
    show_map = OWM_SHOW_MAP
    context = {
        "locations": locations,
        "show_map": show_map,
    }
    return render(request, "django_owm/list_locations.html", context)


def create_location(request):
    """View to create a new weather location."""
    if request.method == "POST":
        form = WeatherLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("django_owm:list_locations")
    else:
        form = WeatherLocationForm()
    context = {
        "form": form,
    }
    return render(request, "django_owm/create_location.html", context)


def delete_location(request, location_id: Union[int, uuid.UUID]):
    """View to delete a weather location."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))

    if OWM_USE_UUID:
        location = get_object_or_404(WeatherLocationModel, uuid=location_id)
    else:
        location = get_object_or_404(WeatherLocationModel, pk=location_id)

    if request.method == "POST":
        location.delete()
        return redirect("django_owm:list_locations")

    context = {
        "location": location,
    }
    return render(request, "django_owm/delete_location.html", context)


def update_location(request, location_id: Union[int, uuid.UUID]):
    """View to update a weather location."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))

    if OWM_USE_UUID:
        location = get_object_or_404(WeatherLocationModel, uuid=location_id)
    else:
        location = get_object_or_404(WeatherLocationModel, pk=location_id)

    if request.method == "POST":
        form = WeatherLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect("django_owm:list_locations")
    else:
        form = WeatherLocationForm(instance=location)
    context = {
        "form": form,
        "location": location,
    }
    return render(request, "django_owm/update_location.html", context)


def weather_detail(request, location_id: Union[int, uuid.UUID]):
    """View to display the weather details for a location."""
    model_mappings = OWM_MODEL_MAPPINGS
    WeatherLocationModel = apps.get_model(model_mappings.get("WeatherLocation"))
    CurrentWeatherModel = apps.get_model(model_mappings.get("CurrentWeather"))

    if OWM_USE_UUID:
        location = get_object_or_404(WeatherLocationModel, uuid=location_id)
    else:
        location = get_object_or_404(WeatherLocationModel, pk=location_id)

    current_weather = CurrentWeatherModel.objects.filter(location=location).order_by("-timestamp").first()

    context = {
        "location": location,
        "current_weather": current_weather,
        "show_map": OWM_SHOW_MAP,
    }

    return render(request, "django_owm/weather_detail.html", context)


def weather_history(request, location_id: Union[int, uuid.UUID]):
    """View to display historical weather data for a location."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    CurrentWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))

    if OWM_USE_UUID:
        location = get_object_or_404(WeatherLocationModel, uuid=location_id)
    else:
        location = get_object_or_404(WeatherLocationModel, pk=location_id)

    historical_weather = CurrentWeatherModel.objects.filter(location=location).order_by("-timestamp")

    context = {
        "location": location,
        "historical_weather": historical_weather,
    }

    return render(request, "django_owm/weather_history.html", context)


def weather_forecast(request, location_id: Union[int, uuid.UUID]):
    """View to display weather forecast for a location."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    HourlyWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get("HourlyWeather"))
    DailyWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get("DailyWeather"))

    if OWM_USE_UUID:
        location = get_object_or_404(WeatherLocationModel, uuid=location_id)
    else:
        location = get_object_or_404(WeatherLocationModel, pk=location_id)

    hourly_forecast = HourlyWeatherModel.objects.filter(location=location, timestamp__gte=timezone.now()).order_by(
        "timestamp"
    )
    daily_forecast = DailyWeatherModel.objects.filter(location=location, timestamp__gte=timezone.now()).order_by(
        "timestamp"
    )

    context = {
        "location": location,
        "hourly_forecast": hourly_forecast,
        "daily_forecast": daily_forecast,
    }

    return render(request, "django_owm/weather_forecast.html", context)


def weather_alerts(request, location_id: Union[int, uuid.UUID]):
    """View to display weather alerts for a location."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    WeatherAlertModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherAlert"))

    if OWM_USE_UUID:
        location = get_object_or_404(WeatherLocationModel, uuid=location_id)
    else:
        location = get_object_or_404(WeatherLocationModel, pk=location_id)

    alerts = WeatherAlertModel.objects.filter(location=location, end__gte=timezone.now()).order_by("start")

    context = {
        "location": location,
        "alerts": alerts,
    }

    return render(request, "django_owm/weather_alerts.html", context)


def weather_errors(request, location_id: Union[int, uuid.UUID]):
    """View to display weather errors for a location."""
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    WeatherErrorLogModel = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherErrorLog"))

    if OWM_USE_UUID:
        location = get_object_or_404(WeatherLocationModel, uuid=location_id)
    else:
        location = get_object_or_404(WeatherLocationModel, pk=location_id)

    errors = WeatherErrorLogModel.objects.filter(location=location).order_by("-timestamp")

    context = {
        "location": location,
        "errors": errors,
    }

    return render(request, "django_owm/weather_errors.html", context)
