"""App configuration."""

from django.apps import AppConfig


class DjangoOwmConfig(AppConfig):
    """App configuration for django-owm."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_owm"
