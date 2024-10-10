"""Celery tasks for fetching weather data from OpenWeatherMap API for django_owm."""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .app_settings import OWM_MODEL_MAPPINGS, OWM_API_RATE_LIMITS, OWM_API_KEY,get_model_from_string
from django.apps import apps
import requests
import logging

logger = logging.getLogger(__name__)

def get_api_call_counts(api_name):
    """Get the number of API calls made in the last minute and last month."""
    now = timezone.now()
    one_minute_ago = now - timedelta(minutes=1)
    one_month_ago = now - timedelta(days=30)
    APICallLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get('APICallLog'))
    if not APICallLogModel:
        return 0, 0
    calls_last_minute = APICallLogModel.objects.filter(api_name=api_name, timestamp__gte=one_minute_ago).count()
    calls_last_month = APICallLogModel.objects.filter(api_name=api_name, timestamp__gte=one_month_ago).count()
    return calls_last_minute, calls_last_month

@shared_task
def fetch_current_weather():
    """Fetch current weather data for all locations."""
    rate_limits = OWM_API_RATE_LIMITS.get('one_call', {})
    calls_per_minute = rate_limits.get('calls_per_minute', 60)
    calls_per_month = rate_limits.get('calls_per_month', 1000000)
    api_name = 'one_call'

    calls_last_minute, calls_last_month = get_api_call_counts(api_name)
    if calls_last_minute >= calls_per_minute or calls_last_month >= calls_per_month:
        logger.warning('API call limit exceeded. Skipping fetch_current_weather task.')
        return

    WeatherLocationModel = get_model_from_string(OWM_MODEL_MAPPINGS.get('WeatherLocation'))
    if not WeatherLocationModel:
        logger.error('WeatherLocation model is not configured.')
        return

    locations = WeatherLocationModel.objects.all()
    for location in locations:
        calls_last_minute, _ = get_api_call_counts(api_name)
        if calls_last_minute >= calls_per_minute:
            logger.warning('API call limit per minute exceeded. Stopping fetch_current_weather task.')
            break

        # Make API call
        lat = location.latitude
        lon = location.longitude
        api_key = OWM_API_KEY
        if not api_key:
            logger.error('OpenWeatherMap API key not set. Please set OWM_API_KEY in your settings.')
            return

        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Save data to models
                save_current_weather(location, data)
                # Log API call
                APICallLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get('APICallLog'))
                if APICallLogModel:
                    APICallLogModel.objects.create(api_name=api_name)
            else:
                error_message = f'API call failed with status code {response.status_code}'
                save_error_log(location, api_name, error_message, response.text)
                logger.error(error_message)
        except Exception as e:
            error_message = str(e)
            save_error_log(location, api_name, error_message)
            logger.exception('Error fetching current weather')

def save_current_weather(location, data):
    """Save current weather data to the database."""
    model_mappings = OWM_MODEL_MAPPINGS
    CurrentWeatherModel = get_model_from_string(model_mappings.get('CurrentWeather'))
    WeatherConditionModel = get_model_from_string(model_mappings.get('WeatherCondition'))

    if not CurrentWeatherModel or not WeatherConditionModel:
        logger.error('CurrentWeatherModel or WeatherConditionModel is not configured.')
        return

    current_data = data.get('current', {})
    if not current_data:
        return

    timestamp = timezone.datetime.fromtimestamp(current_data['dt'], tz=timezone.utc)
    current_weather = CurrentWeatherModel.objects.create(
        location=location,
        timestamp=timestamp,
        temp=current_data.get('temp'),
        feels_like=current_data.get('feels_like'),
        pressure=current_data.get('pressure'),
        humidity=current_data.get('humidity'),
        dew_point=current_data.get('dew_point'),
        uvi=current_data.get('uvi'),
        clouds=current_data.get('clouds'),
        visibility=current_data.get('visibility'),
        wind_speed=current_data.get('wind_speed'),
        wind_deg=current_data.get('wind_deg'),
        wind_gust=current_data.get('wind_gust'),
        rain_1h=current_data.get('rain', {}).get('1h'),
        snow_1h=current_data.get('snow', {}).get('1h'),
    )
    # Save weather conditions
    weather_conditions = current_data.get('weather', [])
    for condition in weather_conditions:
        WeatherConditionModel.objects.create(
            weather_data=current_weather,
            condition_id=condition.get('id'),
            main=condition.get('main'),
            description=condition.get('description'),
            icon=condition.get('icon'),
        )

def save_error_log(location, api_name, error_message, response_data=None):
    """Save error log to the database."""
    WeatherErrorLogModel = get_model_from_string(OWM_MODEL_MAPPINGS.get('WeatherErrorLog'))
    if not WeatherErrorLogModel:
        logger.error('WeatherErrorLogModel is not configured.')
        return
    WeatherErrorLogModel.objects.create(
        location=location,
        api_name=api_name,
        error_message=error_message,
        response_data=response_data,
    )
