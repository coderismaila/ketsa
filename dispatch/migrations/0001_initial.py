# Generated by Django 4.1 on 2022-08-22 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0007_alter_powertransformer_voltagerating"),
    ]

    operations = [
        migrations.CreateModel(
            name="LoadReading",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateTimeField(verbose_name="date")),
                ("load_amps", models.FloatField(blank=True, null=True, verbose_name="load (A)")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("L/S", "LOAD SHEDDING"),
                            ("O/S", "OUT OF SERVICE"),
                            ("F/C", "FREQUENCY CONTROL"),
                            ("S/C", "SYSTEM COLLAPSE"),
                            ("O/F", "FAULT"),
                            ("P/O", "PLANNED OUTAGE"),
                            ("IN", "IN CIRCUIT"),
                        ],
                        max_length=3,
                        verbose_name="feeder status",
                    ),
                ),
                (
                    "feeder",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.feeder"
                    ),
                ),
            ],
        ),
    ]
