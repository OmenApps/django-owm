"""Tests for the validators module in the django_owm app."""

from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from src.django_owm.validators import validate_latitude
from src.django_owm.validators import validate_longitude


@pytest.mark.parametrize(
    "value,expected_valid",
    [
        (Decimal("0"), True),
        (Decimal("-180"), True),
        (Decimal("180"), True),
        (Decimal("90"), True),
        (Decimal("-90"), True),
        (Decimal("-180.1"), False),
        (Decimal("180.1"), False),
        (0, False),  # Integer
        (180.0, False),  # Float
        ("180", False),  # String
    ],
)
def test_validate_longitude(value, expected_valid):
    """Test the validate_longitude function."""
    if expected_valid:
        validate_longitude(value)  # Should not raise ValidationError
    else:
        with pytest.raises(ValidationError):
            validate_longitude(value)


@pytest.mark.parametrize(
    "value,expected_valid",
    [
        (Decimal("0"), True),
        (Decimal("-90"), True),
        (Decimal("90"), True),
        (Decimal("45"), True),
        (Decimal("-45"), True),
        (Decimal("-90.1"), False),
        (Decimal("90.1"), False),
        (0, False),  # Integer
        (90.0, False),  # Float
        ("90", False),  # String
    ],
)
def test_validate_latitude(value, expected_valid):
    """Test the validate_latitude function."""
    if expected_valid:
        validate_latitude(value)  # Should not raise ValidationError
    else:
        with pytest.raises(ValidationError):
            validate_latitude(value)


def test_validate_longitude_type_check():
    """Test that validate_longitude raises a ValidationError for non-Decimal values."""
    with pytest.raises(ValidationError) as excinfo:
        validate_longitude(180)
    assert "Longitude must be a Decimal" in str(excinfo.value)


def test_validate_latitude_type_check():
    """Test that validate_latitude raises a ValidationError for non-Decimal values."""
    with pytest.raises(ValidationError) as excinfo:
        validate_latitude(90)
    assert "Latitude must be a Decimal" in str(excinfo.value)
