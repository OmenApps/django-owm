# django-owm Terminology and Definitions

This document provides definitions for key terms and concepts used in the `django-owm` app.

## Weather Data Terms

- **Current Weather**: The most recent weather data for a specific location.
- **Minutely Forecast**: Minute-by-minute weather forecast for the next hour.
- **Hourly Forecast**: Hour-by-hour weather forecast for the next 48 hours.
- **Daily Forecast**: Day-by-day weather forecast for the next 7 days.
- **Weather Alert**: Severe weather warnings or advisories for a specific location.

## API-related Terms

- **OpenWeatherMap**: The third-party service providing weather data through its API.
- **One Call API 3.0**: The specific OpenWeatherMap API used by `django-owm` to fetch weather data.
- **API Key**: A unique identifier required to authenticate and make requests to the OpenWeatherMap API.
- **API Rate Limit**: The maximum number of API requests allowed within a specific time frame.

## Model-related Terms

- **WeatherLocation**: A model representing a geographic location for which weather data is collected.
- **CurrentWeather**: A model storing the current weather conditions for a location.
- **MinutelyWeather**: A model storing minute-by-minute weather forecast data.
- **HourlyWeather**: A model storing hour-by-hour weather forecast data.
- **DailyWeather**: A model storing day-by-day weather forecast data.
- **WeatherAlert**: A model storing severe weather alerts for a location.
- **WeatherErrorLog**: A model for logging errors that occur during weather data fetching or processing.
- **APICallLog**: A model for tracking API calls made to OpenWeatherMap.
