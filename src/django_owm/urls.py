"""URLs for the django_owm app."""

from django.urls import path

from . import views


app_name = "django_owm"  # pylint: disable=C0103

urlpatterns = [
    path("weather/<int:location_id>/", views.weather_detail, name="weather_detail"),
]
