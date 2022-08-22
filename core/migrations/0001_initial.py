# Generated by Django 4.1 on 2022-08-21 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AreaOffice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        error_messages={"unique": "name already assigned to another area office"},
                        max_length=25,
                        unique=True,
                        verbose_name="area office",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        error_messages={"unique": "Code already assigned to another area office"},
                        help_text="Required. 3 characters uniqe code",
                        max_length=5,
                        unique=True,
                        verbose_name="code",
                    ),
                ),
                (
                    "technical_manager",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=75, unique=True, verbose_name="name")),
                ("capacity_kva", models.PositiveIntegerField(blank=True, null=True, verbose_name="capacity (kva)")),
                (
                    "type",
                    models.CharField(
                        choices=[("DR", "Distribution"), ("TR", "Transmission")], default="DR", max_length=2
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone_number", models.CharField(max_length=14, verbose_name="phone number")),
                ("personal_email", models.EmailField(max_length=254, verbose_name="personal email")),
                (
                    "gender",
                    models.CharField(choices=[("M", "Male"), ("F", "Female")], max_length=1, verbose_name="gender"),
                ),
                ("birth_date", models.DateField(verbose_name="date of birth")),
                (
                    "area_office",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.areaoffice"),
                ),
                (
                    "station",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.station"),
                ),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PowerTransformer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                ("capacity_kva", models.PositiveIntegerField(verbose_name="capacity (kva)")),
                (
                    "voltageRating",
                    models.CharField(
                        choices=[("330/132KV", "330/132KV"), ("132/33KV", "132/33KV"), ("33/11KV", "132/11KV")],
                        default="33/11KV",
                        max_length=9,
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.station"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Feeder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=50, unique=True, verbose_name="feeder name")),
                ("route_length", models.FloatField(blank=True, null=True, verbose_name="route length")),
                ("kaedco_code", models.CharField(max_length=4, unique=True, verbose_name="kaedco code")),
                ("nerc_code", models.CharField(max_length=4, unique=True, verbose_name="nerc code")),
                (
                    "area_office",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.areaoffice"),
                ),
                (
                    "power_transformer",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.powertransformer"
                    ),
                ),
            ],
        ),
    ]