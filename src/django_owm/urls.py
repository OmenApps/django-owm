"""URLs for the django_owm app."""

from django.urls import path

from . import views
from .app_settings import OWM_USE_UUID


app_name = "django_owm"

if OWM_USE_UUID:
    urlpatterns = [
        path("locations/", views.list_locations, name="list_locations"),
        path("locations/create/", views.create_location, name="create_location"),
        path("locations/<uuid:location_id>/delete/", views.delete_location, name="delete_location"),
        path("locations/<uuid:location_id>/update/", views.update_location, name="update_location"),
        path("weather/<uuid:location_id>/", views.weather_detail, name="weather_detail"),
        path("weather/<uuid:location_id>/history/", views.weather_history, name="weather_history"),
        path("weather/<uuid:location_id>/forecast/", views.weather_forecast, name="weather_forecast"),
        path("weather/<uuid:location_id>/alerts/", views.weather_alerts, name="weather_alerts"),
        path("weather/<uuid:location_id>/errors/", views.weather_errors, name="weather_errors"),
        path(
            "weather/<uuid:location_id>/history/partial/", views.weather_history_partial, name="weather_history_partial"
        ),
        path(
            "weather/<uuid:location_id>/forecast/partial/",
            views.weather_forecast_partial,
            name="weather_forecast_partial",
        ),
        path("weather/<uuid:location_id>/alerts/partial/", views.weather_alerts_partial, name="weather_alerts_partial"),
        path("weather/<uuid:location_id>/errors/partial/", views.weather_errors_partial, name="weather_errors_partial"),
    ]
else:
    urlpatterns = [
        path("locations/", views.list_locations, name="list_locations"),
        path("locations/create/", views.create_location, name="create_location"),
        path("locations/<int:location_id>/delete/", views.delete_location, name="delete_location"),
        path("locations/<int:location_id>/update/", views.update_location, name="update_location"),
        path("weather/<int:location_id>/", views.weather_detail, name="weather_detail"),
        path("weather/<int:location_id>/history/", views.weather_history, name="weather_history"),
        path("weather/<int:location_id>/forecast/", views.weather_forecast, name="weather_forecast"),
        path("weather/<int:location_id>/alerts/", views.weather_alerts, name="weather_alerts"),
        path("weather/<int:location_id>/errors/", views.weather_errors, name="weather_errors"),
        path(
            "weather/<int:location_id>/history/partial/", views.weather_history_partial, name="weather_history_partial"
        ),
        path(
            "weather/<int:location_id>/forecast/partial/",
            views.weather_forecast_partial,
            name="weather_forecast_partial",
        ),
        path("weather/<int:location_id>/alerts/partial/", views.weather_alerts_partial, name="weather_alerts_partial"),
        path("weather/<int:location_id>/errors/partial/", views.weather_errors_partial, name="weather_errors_partial"),
    ]
