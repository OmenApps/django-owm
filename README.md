# django-owm

[![PyPI](https://img.shields.io/pypi/v/django-own.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/django-owm.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/django-owm)][pypi status]
[![License](https://img.shields.io/pypi/l/django-owm)][license]

[![Read the documentation at https://django-owm.readthedocs.io/](https://img.shields.io/readthedocs/django-owm/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/OmenApps/django-owm/actions/workflows/tests.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/OmenApps/django-owm/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/django-owm/
[read the docs]: https://django-owm.readthedocs.io/
[tests]: https://github.com/OmenApps/django-owm/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/OmenApps/django-owm
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

`django-owm` is a reusable Django app for fetching and storing weather data from the OpenWeatherMap One Call 3.0 API. It provides a simple interface for managing weather locations, fetching current, historical, and forecast weather data, and displaying this information in your Django project.

## Features

- Fetch and store weather data from OpenWeatherMap One Call API 3.0
- Support for current, minutely, hourly, and daily weather data
- Weather alerts tracking
- Customizable models for storing weather data
- Management commands for easy interaction with the app
- Celery tasks for automated weather data fetching
- Built-in views and templates for displaying weather information
- Flexible configuration options

## Requirements

- TODO

## Installation

1. Install the package using pip:

```bash
pip install django-owm
```

2. Add `'django_owm'` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    ...
    'django_owm',
]
```

## Configuration

Add the following settings to your Django project's `settings.py` file:

```python
DJANGO_OWM = {
    'OWM_API_KEY': 'your_openweathermap_api_key',
    'OWM_API_RATE_LIMITS': {
        'one_call': {
            'calls_per_minute': 60,
            'calls_per_month': 1000000,
        },
    },
    'OWM_MODEL_MAPPINGS': {
        'WeatherLocation': 'your_app.WeatherLocation',
        'CurrentWeather': 'your_app.CurrentWeather',
        'MinutelyWeather': 'your_app.MinutelyWeather',
        'HourlyWeather': 'your_app.HourlyWeather',
        'DailyWeather': 'your_app.DailyWeather',
        'WeatherAlert': 'your_app.WeatherAlert',
        'WeatherErrorLog': 'your_app.WeatherErrorLog',
        'APICallLog': 'your_app.APICallLog',
    },
    'OWM_BASE_MODEL': models.Model,
    'OWM_USE_BUILTIN_ADMIN': True,
    'OWM_SHOW_MAP': False,
    'OWM_USE_UUID': False,
}
```

Replace `'your_openweathermap_api_key'` with your actual OpenWeatherMap API key, and adjust the model mappings to point to your custom model implementations if you're not using the default models.

See the [Usage Reference] for more details.

## Migrate Database

Run migrations to create the necessary database tables:

```bash
python manage.py migrate
```

## Quick Start

1. Create a new weather location:

```bash
python manage.py create_location
```

2. Fetch weather data for all locations:

```bash
python manage.py manual_weather_fetch
```

3. View the weather data in the Django admin interface or use the provided views to display the information in your templates.

## Customization

### Models

You can customize the models used by `django-owm` by creating your own models that inherit from the abstract base models provided by the app. Update the `OWM_MODEL_MAPPINGS` in your settings to use your custom models.

### Views and Templates

`django-owm` provides basic views and templates for displaying weather information. You can override these templates by creating your own templates with the same names in your project's template directory.

### Celery Tasks

To set up automated weather data fetching, configure Celery in your project and add the following task to your `CELERYBEAT_SCHEDULE`:

```python
CELERYBEAT_SCHEDULE = {
    'fetch_weather_data': {
        'task': 'django_owm.tasks.fetch_weather',
        'schedule': crontab(minute='*/30'),  # Run every 30 minutes
    },
}
```

Please see the [Usage Reference] for further details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_django-owm_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@OmenApps]'s [Cookiecutter Django Package] template.

[@omenapps]: https://github.com/OmenApps
[pypi]: https://pypi.org/
[cookiecutter django package]: https://github.com/OmenApps/cookiecutter-django-package
[file an issue]: https://github.com/OmenApps/django-owm/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/OmenApps/django-owm/blob/main/LICENSE
[contributor guide]: https://github.com/OmenApps/django-owm/blob/main/CONTRIBUTING.md
[usage reference]: https://django-owm.readthedocs.io/en/latest/usage.html
