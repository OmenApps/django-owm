"""Tests for app_settings.py in the django_owm app."""


def test_app_settings_defaults(monkeypatch):
    """Test that default settings are used when specific settings are missing."""
    monkeypatch.setattr("django.conf.settings.DJANGO_OWM", {})
    from src.django_owm.app_settings import OWM_API_RATE_LIMITS  # pylint: disable=C0415
    from src.django_owm.app_settings import (
        OWM_USE_BUILTIN_ADMIN,  # pylint: disable=C0415
    )

    assert OWM_API_RATE_LIMITS == {"one_call": {"calls_per_minute": 60, "calls_per_month": 1000000}}
    assert OWM_USE_BUILTIN_ADMIN is True
