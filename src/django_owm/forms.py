"""Forms for django_owm."""

from django import forms

from .app_settings import OWM_MODEL_MAPPINGS
from .app_settings import get_model_from_string


class WeatherLocationForm(forms.ModelForm):
    """Form for creating or updating a Weather Location."""

    class Meta:
        """Meta class for WeatherLocationForm."""

        model = get_model_from_string(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
        fields = ["name", "latitude", "longitude"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
