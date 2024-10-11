"""Tests for the admin module in the django_owm app."""

import importlib

from django.contrib.admin.sites import site

from src.django_owm.app_settings import OWM_MODEL_MAPPINGS
from src.django_owm.app_settings import get_model_from_string


def test_admin_model_registration():
    """Test that models are registered in the admin site."""
    WeatherLocation = get_model_from_string(OWM_MODEL_MAPPINGS["WeatherLocation"])  # pylint: disable=C0103
    assert WeatherLocation in site._registry  # Accessing the private _registry attribute
