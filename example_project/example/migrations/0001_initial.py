# Generated by Django 4.2.16 on 2024-10-10 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="APICallLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("api_name", models.CharField(max_length=255)),
                (
                    "units",
                    models.CharField(
                        choices=[("standard", "Standard"), ("metric", "Metric"), ("imperial", "Imperial")],
                        default="standard",
                        max_length=10,
                        verbose_name="Units",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="WeatherLocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=255, null=True, verbose_name="Location Name")),
                (
                    "latitude",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Latitude of the location, decimal (−90; 90)",
                        max_digits=5,
                        verbose_name="Latitude",
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Longitude of the location, decimal (−180; 180)",
                        max_digits=5,
                        verbose_name="Longitude",
                    ),
                ),
                (
                    "timezone",
                    models.CharField(
                        blank=True,
                        help_text="Timezone name for the requested location",
                        max_length=255,
                        null=True,
                        verbose_name="Timezone",
                    ),
                ),
                (
                    "timezone_offset",
                    models.IntegerField(
                        blank=True, help_text="Offset from UTC in seconds", null=True, verbose_name="Timezone Offset"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="WeatherErrorLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("api_name", models.CharField(max_length=255)),
                ("error_message", models.TextField()),
                ("response_data", models.TextField(blank=True, null=True)),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="error_logs",
                        to="example.weatherlocation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="WeatherAlert",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sender_name", models.CharField(max_length=255)),
                ("event", models.CharField(max_length=255)),
                ("start", models.DateTimeField(help_text="Start time of the alert", verbose_name="Start Time")),
                ("end", models.DateTimeField(help_text="End time of the alert", verbose_name="End Time")),
                ("description", models.TextField()),
                ("tags", models.JSONField(blank=True, default=list, null=True)),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weather_alerts",
                        to="example.weatherlocation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MinutelyWeather",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "timestamp",
                    models.DateTimeField(help_text="Unix timestamp converted to DateTime", verbose_name="Timestamp"),
                ),
                ("precipitation", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Precipitation")),
                (
                    "location",
                    models.ForeignKey(
                        help_text="Location for this weather data by minute",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="minutely_weather",
                        to="example.weatherlocation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="HourlyWeather",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "timestamp",
                    models.DateTimeField(help_text="Unix timestamp converted to DateTime", verbose_name="Timestamp"),
                ),
                ("pressure", models.IntegerField(blank=True, null=True)),
                ("humidity", models.IntegerField(blank=True, null=True)),
                (
                    "dew_point",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Dew Point"
                    ),
                ),
                (
                    "uvi",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="UV Index"),
                ),
                ("clouds", models.IntegerField(blank=True, null=True)),
                (
                    "wind_speed",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Wind Speed"
                    ),
                ),
                ("wind_deg", models.IntegerField(blank=True, null=True)),
                (
                    "wind_gust",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Wind Gust"
                    ),
                ),
                ("weather_condition_id", models.IntegerField()),
                ("weather_condition_main", models.CharField(max_length=255)),
                ("weather_condition_description", models.CharField(help_text="Icon description", max_length=255)),
                ("weather_condition_icon", models.CharField(max_length=10)),
                (
                    "temp",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Temperature"
                    ),
                ),
                (
                    "feels_like",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Feels Like Temperature"
                    ),
                ),
                ("visibility", models.IntegerField(blank=True, null=True)),
                (
                    "pop",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        verbose_name="Probability of Precipitation",
                    ),
                ),
                (
                    "rain_1h",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Rain (1h)"
                    ),
                ),
                (
                    "snow_1h",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Snow (1h)"
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        help_text="Location for this weather data",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_weather_data",
                        related_query_name="%(app_label)s_%(class)ss",
                        to="example.weatherlocation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DailyWeather",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "timestamp",
                    models.DateTimeField(help_text="Unix timestamp converted to DateTime", verbose_name="Timestamp"),
                ),
                ("pressure", models.IntegerField(blank=True, null=True)),
                ("humidity", models.IntegerField(blank=True, null=True)),
                (
                    "dew_point",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Dew Point"
                    ),
                ),
                (
                    "uvi",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="UV Index"),
                ),
                ("clouds", models.IntegerField(blank=True, null=True)),
                (
                    "wind_speed",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Wind Speed"
                    ),
                ),
                ("wind_deg", models.IntegerField(blank=True, null=True)),
                (
                    "wind_gust",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Wind Gust"
                    ),
                ),
                ("weather_condition_id", models.IntegerField()),
                ("weather_condition_main", models.CharField(max_length=255)),
                ("weather_condition_description", models.CharField(help_text="Icon description", max_length=255)),
                ("weather_condition_icon", models.CharField(max_length=10)),
                ("sunrise", models.DateTimeField(blank=True, null=True)),
                ("sunset", models.DateTimeField(blank=True, null=True)),
                ("moonrise", models.DateTimeField(blank=True, null=True)),
                ("moonset", models.DateTimeField(blank=True, null=True)),
                (
                    "moon_phase",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Moon Phase"
                    ),
                ),
                ("summary", models.TextField(blank=True, null=True)),
                (
                    "temp_min",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Temperature Min"
                    ),
                ),
                (
                    "temp_max",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Temperature Max"
                    ),
                ),
                (
                    "temp_morn",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Morning Temperature"
                    ),
                ),
                (
                    "temp_day",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Day Temperature"
                    ),
                ),
                (
                    "temp_eve",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Evening Temperature"
                    ),
                ),
                (
                    "temp_night",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Night Temperature"
                    ),
                ),
                (
                    "feels_like_morn",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Feels Like - Morning"
                    ),
                ),
                (
                    "feels_like_day",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Feels Like - Day"
                    ),
                ),
                (
                    "feels_like_eve",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Feels Like - Evening"
                    ),
                ),
                (
                    "feels_like_night",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Feels Like - Night"
                    ),
                ),
                (
                    "pop",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        verbose_name="Probability of Precipitation",
                    ),
                ),
                (
                    "rain",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Rain"),
                ),
                (
                    "snow",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Snow"),
                ),
                (
                    "location",
                    models.ForeignKey(
                        help_text="Location for this weather data",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_weather_data",
                        related_query_name="%(app_label)s_%(class)ss",
                        to="example.weatherlocation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CurrentWeather",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "timestamp",
                    models.DateTimeField(help_text="Unix timestamp converted to DateTime", verbose_name="Timestamp"),
                ),
                ("pressure", models.IntegerField(blank=True, null=True)),
                ("humidity", models.IntegerField(blank=True, null=True)),
                (
                    "dew_point",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Dew Point"
                    ),
                ),
                (
                    "uvi",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="UV Index"),
                ),
                ("clouds", models.IntegerField(blank=True, null=True)),
                (
                    "wind_speed",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Wind Speed"
                    ),
                ),
                ("wind_deg", models.IntegerField(blank=True, null=True)),
                (
                    "wind_gust",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Wind Gust"
                    ),
                ),
                ("weather_condition_id", models.IntegerField()),
                ("weather_condition_main", models.CharField(max_length=255)),
                ("weather_condition_description", models.CharField(help_text="Icon description", max_length=255)),
                ("weather_condition_icon", models.CharField(max_length=10)),
                ("sunrise", models.DateTimeField(blank=True, null=True)),
                ("sunset", models.DateTimeField(blank=True, null=True)),
                (
                    "temp",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Temperature"
                    ),
                ),
                (
                    "feels_like",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="Feels Like Temperature"
                    ),
                ),
                ("visibility", models.IntegerField(blank=True, null=True)),
                (
                    "rain_1h",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Precipitation in mm/h",
                        max_digits=5,
                        null=True,
                        verbose_name="Rain (1h)",
                    ),
                ),
                (
                    "snow_1h",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Snowfall in mm/h",
                        max_digits=5,
                        null=True,
                        verbose_name="Snow (1h)",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        help_text="Location for this weather data",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_weather_data",
                        related_query_name="%(app_label)s_%(class)ss",
                        to="example.weatherlocation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
