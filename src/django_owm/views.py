"""Views for the django_owm app."""
from django.shortcuts import render, get_object_or_404
from .app_settings import OWM_MODEL_MAPPINGS
from django.apps import apps

def weather_detail(request, location_id):
    model_mappings = OWM_MODEL_MAPPINGS
    WeatherLocationModel = apps.get_model(model_mappings.get('WeatherLocation'))
    CurrentWeatherModel = apps.get_model(model_mappings.get('CurrentWeather'))

    location = get_object_or_404(WeatherLocationModel, pk=location_id)
    current_weather = CurrentWeatherModel.objects.filter(location=location).order_by('-timestamp').first()

    context = {
        'location': location,
        'current_weather': current_weather,
    }

    return render(request, 'django_owm/weather_detail.html', context)
