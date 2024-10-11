# Using django-owm

This guide provides detailed instructions on how to use the `django-owm` app in your Django project.

## 1. Setting Up Weather Locations

Before you can fetch weather data, you need to set up one or more weather locations.

### Using the Management Command

```bash
python manage.py create_location
```

This command will prompt you to enter the location name, latitude, and longitude.

### Using the Django Admin

1. Navigate to the Django admin interface.
2. Click on "Weather locations" under the "Django_owm" section.
3. Click "Add weather location" and fill in the required information.

### Using the Provided View

1. Navigate to `/owm/locations/create/` in your browser.
2. Fill out the form with the location details and submit.

## 2. Fetching Weather Data

### Manual Fetching

To manually fetch weather data for all locations:

```bash
python manage.py manual_weather_fetch
```

To fetch data for a specific location:

```bash
python manage.py manual_weather_fetch <location_id>
```

### Automated Fetching with Celery

If you've set up Celery and configured the periodic task as described in the README, weather data will be fetched automatically according to your specified schedule.

## 3. Viewing Weather Data

### Using the Django Admin

1. Navigate to the Django admin interface.
2. Click on the desired weather data model (e.g., "Current weathers", "Hourly weathers", etc.) under the "Django_owm" section.
3. You can view and filter the weather data for different locations and timestamps.

### Using the Provided Views

- List all locations: `/owm/locations/`
- Weather detail for a location: `/owm/weather/<location_id>/`

## 4. Customizing the App

### Overriding Templates

To customize the appearance of the provided views, create your own templates in your project's template directory with the same names as the `django-owm` templates. For example:

- `templates/django_owm/list_locations.html`
- `templates/django_owm/weather_detail.html`
- `templates/django_owm/weather_forecast.html`

### Extending Models

To add custom fields or methods to the weather data models:

1. Create your own models that inherit from the `django-owm` abstract models.
2. Update the `OWM_MODEL_MAPPINGS` in your project's settings to use your custom models.

Example:

```python
from django_owm.models import AbstractCurrentWeather

class CustomCurrentWeather(AbstractCurrentWeather):
    custom_field = models.CharField(max_length=100)

    class Meta:
        abstract = False

# In your settings.py
DJANGO_OWM = {
    # ...
    'OWM_MODEL_MAPPINGS': {
        # ...
        'CurrentWeather': 'your_app.CustomCurrentWeather',
        # ...
    },
    # ...
}
```

### Creating Custom Views

You can create your own views to display weather data in a custom format or to integrate it with other parts of your application. Use the `django-owm` models to query the weather data as needed.

Example:

```python
from django.shortcuts import render
from django_owm.app_settings import OWM_MODEL_MAPPINGS
from django.apps import apps

def custom_weather_view(request, location_id):
    WeatherLocationModel = apps.get_model(OWM_MODEL_MAPPINGS.get('WeatherLocation'))
    CurrentWeatherModel = apps.get_model(OWM_MODEL_MAPPINGS.get('CurrentWeather'))

    location = WeatherLocationModel.objects.get(pk=location_id)
    current_weather = CurrentWeatherModel.objects.filter(location=location).latest('timestamp')

    context = {
        'location': location,
        'current_weather': current_weather,
    }
    return render(request, 'your_app/custom_weather_template.html', context)
```

## 5. Troubleshooting

- If you're not seeing any weather data, ensure that you've set up at least one weather location and run the `manual_weather_fetch` command or waited for the Celery task to execute.
- Check the `WeatherErrorLog` model in the Django admin for any errors that occurred during weather data fetching.
- Verify that your OpenWeatherMap API key is correct and that you haven't exceeded your API rate limits.

By following this guide, you should be able to effectively use and customize the `django-owm` app in your Django project. If you encounter any issues or have questions, please refer to the project's documentation or open an issue on the GitHub repository.
