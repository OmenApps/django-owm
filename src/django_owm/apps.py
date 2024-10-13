"""App configuration for the django_owm app."""

from django.apps import AppConfig
from django.core.checks import Error
from django.core.checks import register

from .app_settings import OWM_API_KEY
from .app_settings import OWM_MODEL_MAPPINGS


class DjangoOwmConfig(AppConfig):
    """App configuration for django-owm."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.django_owm"

    def ready(self):
        """Run when the app is ready."""

        def check_model_mappings(app_configs, **kwargs):  # pylint: disable=W0613
            """Check that all model mappings are set."""
            errors = []
            for model_name in [
                "WeatherLocation",
                "CurrentWeather",
                "MinutelyWeather",
                "HourlyWeather",
                "DailyWeather",
                "WeatherAlert",
                "WeatherErrorLog",
                "APICallLog",
            ]:
                model_string = OWM_MODEL_MAPPINGS.get(model_name)
                if not model_string:
                    errors.append(
                        Error(
                            f"Model mapping for {model_name} is not set.",
                            hint=f"Set OWM_MODEL_MAPPINGS['{model_name}'] in your settings.",  # noqa: B907
                            obj=self,
                            id="django_owm.E001",
                        )
                    )
            return errors

        def check_api_key(app_configs, **kwargs):  # pylint: disable=W0613
            """Check that the API key is set."""
            if not OWM_API_KEY:
                return [
                    Error(
                        "OpenWeatherMap API key is not set.",
                        hint="Set OWM_API_KEY in your settings.",
                        obj=self,
                        id="django_owm.E002",
                    )
                ]
            return []

        register(check_model_mappings)
        register(check_api_key)
