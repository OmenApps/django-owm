"""Forms for django_owm."""

from decimal import ROUND_HALF_UP
from decimal import Decimal
from decimal import DecimalException

from django import forms
from django.apps import apps
from django.forms.fields import DecimalField

from .app_settings import OWM_MODEL_MAPPINGS
from .validators import validate_latitude
from .validators import validate_longitude


def quantize_to_2_decimal_places(value: Decimal | str | None) -> Decimal | None:
    """Quantize a Decimal value to 2 decimal places."""
    if value is not None:
        if isinstance(value, str):
            try:
                value = Decimal(value)
            except DecimalException:
                return value
        if isinstance(value, Decimal):
            return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        raise ValueError("Value must be a Decimal or a string that can be converted to a Decimal.")
    return value


class TrimmedDecimalField(DecimalField):
    """Custom DecimalField that trims the value to 2 decimal places."""

    def to_python(self, value):
        """Trim the value to 2 decimal places."""
        value = super().to_python(value)
        if value is not None:
            return quantize_to_2_decimal_places(value)
        return value


class WeatherLocationForm(forms.ModelForm):
    """Form for creating or updating a Weather Location."""

    latitude = TrimmedDecimalField(
        max_digits=5,
        decimal_places=2,
        required=True,
        label="Latitude",
        help_text="Enter the latitude of the location (e.g., 40.7128)",
    )
    longitude = TrimmedDecimalField(
        max_digits=5,
        decimal_places=2,
        required=True,
        label="Longitude",
        help_text="Enter the longitude of the location (e.g., -74.0060)",
    )

    class Meta:
        """Meta class for WeatherLocationForm."""

        model = apps.get_model(OWM_MODEL_MAPPINGS.get("WeatherLocation"))
        fields = ["name", "latitude", "longitude"]

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False

    def clean_latitude(self):
        """Clean the input latitude value."""
        latitude = self.cleaned_data.get("latitude")
        # Validate the latitude value is a Decimal within the valid range
        validate_latitude(latitude)
        return latitude

    def clean_longitude(self):
        """Clean the input longitude value."""
        longitude = self.cleaned_data.get("longitude")
        # Validate the longitude value is a Decimal within the valid range
        validate_longitude(longitude)
        return longitude
