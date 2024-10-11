"""Tests for the admin module in the django_owm app."""

from django.apps import apps
from django.contrib.admin.sites import site

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS


def test_admin_model_registration():
    """Test that models are registered in the admin site."""
    WeatherLocation = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
    assert WeatherLocation in site._registry  # pylint: disable=W0212
