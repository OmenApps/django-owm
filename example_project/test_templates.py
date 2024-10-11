"""Tests for template rendering in the django_owm app."""

from django.apps import apps
from django.template import Context
from django.template import Template

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS


def test_weather_detail_template_rendering():
    """Test that weather_detail template renders correctly."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    CurrentWeather = apps.get_model(OWM_MODEL_MAPPINGS.get("CurrentWeather"))

    location = WeatherLocation(name="Test Location", latitude=10.0, longitude=20.0, timezone="UTC")
    current_weather = CurrentWeather(
        location=location,
        temp=295.15,
        weather_condition_main="Clear",
    )

    template_content = """
    {% extends "django_owm/base.html" %}
    {% block content %}
    <h1>{{ location.name }}</h1>
    <p>Temperature: {{ current_weather.temp }} K</p>
    {% endblock %}
    """
    template = Template(template_content)
    context = Context(
        {
            "location": location,
            "current_weather": current_weather,
        }
    )
    rendered = template.render(context)
    assert "Test Location" in rendered
    assert "Temperature: 295.15 K" in rendered


def test_weather_detail_template_empty_context():
    """Test that weather_detail template handles empty context."""
    template_content = """
    {% extends "django_owm/base.html" %}
    {% block content %}
    {% if location %}
    <h1>{{ location.name }}</h1>
    {% else %}
    <p>No location provided.</p>
    {% endif %}
    {% endblock %}
    """
    template = Template(template_content)
    context = Context({})
    rendered = template.render(context)
    assert "No location provided." in rendered
