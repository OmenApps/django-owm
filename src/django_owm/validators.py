"""Validators for the models of the django_owm app."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_longitude(value):
    """Validate that the longitude is between -180 and 180."""
    if not isinstance(value, Decimal):
        raise ValidationError(
            _("Longitude must be a Decimal"),
        )

    if value < Decimal("-180") or value > Decimal("180"):
        raise ValidationError(
            _("Longitude must be between -180 and 180"),
        )


def validate_latitude(value):
    """Validate that the latitude is between -90 and 90."""
    if not isinstance(value, Decimal):
        raise ValidationError(
            _("Latitude must be a Decimal"),
        )

    if value < Decimal("-90") or value > Decimal("90"):
        raise ValidationError(
            _("Latitude must be between -90 and 90"),
        )
