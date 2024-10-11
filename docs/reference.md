# Reference

This document provides a detailed overview of the components of `django-owm`.

## Table of Contents

- [Reference](#reference)
  - [Table of Contents](#table-of-contents)
    - [Models](#models)
    - [Management Commands](#management-commands)
    - [Utility Functions](#utility-functions)
    - [App Settings](#app-settings)
      - [Example Settings Dictionary](#example-settings-dictionary)
    - [Views](#views)
    - [Admin](#admin)

### Models

The `django-owm` app includes several abstract models that developers can use or extend for storing weather data:

- **AbstractWeatherLocation**: Stores information about the locations for which weather data is collected.
- **AbstractCurrentWeather**: Stores current weather data for a given location.
- **AbstractMinutelyWeather**: Stores weather data at minute intervals.
- **AbstractHourlyWeather**: Stores hourly weather data.
- **AbstractDailyWeather**: Stores daily weather data, including sunrise/sunset information.
- **AbstractWeatherAlert**: Stores alerts issued for the weather in a particular location.
- **AbstractWeatherErrorLog**: Stores information about errors encountered when fetching weather data.
- **AbstractAPICallLog**: Stores information about API calls made for weather data collection.

These models are all abstract, allowing developers to customize their own concrete versions as needed.

### Management Commands

The app provides several management commands to interact with the weather data models:

- **create\_location**: Creates a new weather location.

  - **Input Parameters**:
    - **name** (str): The name of the location.
    - **latitude** (float): The latitude of the location.
    - **longitude** (float): The longitude of the location.
    - **timezone** (str, optional): The timezone of the location.

- **delete\_location**: Deletes a specified weather location.

  - **Input Parameters**:
    - **location\_id** (int or UUID): The ID of the location to delete.

- **list\_locations**: Lists all weather locations stored in the database.

  - **Input Parameters**: None.

- **manual\_weather\_fetch**: Manually fetches weather data for a specific location.

  - **Input Parameters**:
    - **location\_id** (int or UUID): The ID of the location for which to fetch weather data.

These commands help developers easily manage the locations for which weather data is collected.

### Utility Functions

The `utils` module provides various utility functions to interact with the OpenWeatherMap API and save data:

- **API Interaction**: Functions such as `make_api_call` for making requests to OpenWeatherMap, and `check_api_limits` to enforce API rate limits.
- **Data Saving**: Functions such as `save_weather_data`, `save_current_weather`, `save_hourly_weather`, etc., for storing weather data in the database.
- **Error Logging**: Function `save_error_log` to log errors encountered when fetching weather data.

### App Settings

The settings for the `django-owm` app are defined in `app_settings.py`, allowing flexibility for customization:

- **OWM\_API\_KEY** (default: `None`): A string representing the API key used to make requests to OpenWeatherMap. This key is required for the app to function properly, as it authorizes API requests.

  - **Type**: `str`
  - **Example**: `OWM_API_KEY = "your_openweathermap_api_key_here"`
  - **Why Set**: Developers need to provide their own API key to connect to the OpenWeatherMap API.

- **OWM\_API\_RATE\_LIMITS** (default: `{ "one_call": { "calls_per_minute": 60, "calls_per_month": 1000000 } }`): A dictionary defining the rate limits for the API calls, including calls per minute and per month. This helps manage API usage effectively.

  - **Type**: `dict`
  - **Example**:
    ```python
    OWM_API_RATE_LIMITS = {
        "one_call": {
            "calls_per_minute": 60,
            "calls_per_month": 1000000,
        },
    }
    ```
  - **Why Set**: To ensure that the app respects the rate limits of the OpenWeatherMap API and prevents exceeding them, which could result in blocked access.

- **OWM\_MODEL\_MAPPINGS** (default: `{}`): A dictionary mapping abstract models to concrete model implementations in the developer's application. This setting allows developers to customize the data storage by specifying their own models. **Note: All models must be mapped in ********`OWM_MODEL_MAPPINGS`******** for the app to function correctly.**

  - **Type**: `dict`
  - **Example**:
    ```python
    OWM_MODEL_MAPPINGS = {
        "WeatherLocation": "myapp.CustomWeatherLocation",
        "CurrentWeather": "myapp.CustomCurrentWeather",
        "MinutelyWeather": "myapp.CustomMinutelyWeather",
        "HourlyWeather": "myapp.CustomHourlyWeather",
        "DailyWeather": "myapp.CustomDailyWeather",
        "WeatherAlert": "myapp.CustomWeatherAlert",
        "WeatherErrorLog": "myapp.CustomWeatherErrorLog",
        "APICallLog": "myapp.CustomAPICallLog",
    }
    ```
  - **Why Set**: Developers must provide mappings for all abstract models to ensure the app's functionality. This allows them to extend or modify the behavior of default models to fit the specific requirements of their application.

- **OWM\_USE\_BUILTIN\_ADMIN** (default: `True`): A boolean that controls whether built-in Django admin views should be used for the models.

  - **Type**: `bool`
  - **Example**: `OWM_USE_BUILTIN_ADMIN = False`
  - **Why Set**: If developers prefer to create custom admin interfaces for managing weather data, they can set this to `False` and override the default behavior.

- **OWM\_USE\_UUID** (default: `False`): A boolean that configures whether a `uuid` field should be added to the models for querying and data uniqueness.

  - **Type**: `bool`
  - **Example**: `OWM_USE_UUID = True`
  - **Why Set**: Developers may choose to use UUIDs for models to enhance data uniqueness and security, particularly in distributed systems.

#### Example Settings Dictionary

```python
DJANGO_OWM = {
    "OWM_API_KEY": "your_openweathermap_api_key_here",
    "OWM_API_RATE_LIMITS": {
        "one_call": {
            "calls_per_minute": 60,
            "calls_per_month": 1000000,
        },
    },
    "OWM_MODEL_MAPPINGS": {
        "WeatherLocation": "myapp.CustomWeatherLocation",
        "CurrentWeather": "myapp.CustomCurrentWeather",
        "MinutelyWeather": "myapp.CustomMinutelyWeather",
        "HourlyWeather": "myapp.CustomHourlyWeather",
        "DailyWeather": "myapp.CustomDailyWeather",
        "WeatherAlert": "myapp.CustomWeatherAlert",
        "WeatherErrorLog": "myapp.CustomWeatherErrorLog",
        "APICallLog": "myapp.CustomAPICallLog",
    },
    "OWM_USE_BUILTIN_ADMIN": True,
    "OWM_USE_UUID": False,
}
```

These settings provide a flexible and extensible approach to managing the app's configuration, allowing developers to tailor the behavior and data models of the `django-owm` app to meet the needs of their specific project.

### Views

The app provides several function-based views for displaying weather data:

- **list\_locations**: Displays a list of all weather locations.
- **create\_location**: Allows users to create a new weather location.
- **update\_location**: Allows users to update an existing location's details.
- **delete\_location**: Deletes a specified weather location.
- **weather\_detail**: Displays current weather details for a specified location.
- **weather\_history**: Displays historical weather data.
- **weather\_forecast**: Shows hourly and daily forecasts for a location.
- **weather\_alerts**: Displays any active weather alerts for a location.
- **weather\_errors**: Shows logged errors encountered when fetching data.

These views are designed to be easily customizable and integrate seamlessly with Django templates.

### Admin

The app provides built-in Django admin support for the weather data models, including:

- **WeatherLocationAdmin**: Manage weather locations.
- **CurrentWeatherAdmin**: View and manage current weather data
