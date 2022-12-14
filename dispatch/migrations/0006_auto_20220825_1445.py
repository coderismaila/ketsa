# Generated by Django 3.2.15 on 2022-08-25 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dispatch", "0005_alter_forcedoutage_relay_indicator"),
    ]

    operations = [
        migrations.AddField(
            model_name="loadreading",
            name="allocation_mw",
            field=models.FloatField(blank=True, null=True, verbose_name="allocation (MW)"),
        ),
        migrations.AddField(
            model_name="loadreading",
            name="generation_mw",
            field=models.FloatField(blank=True, null=True, verbose_name="generation (MW)"),
        ),
        migrations.AlterField(
            model_name="loadreading",
            name="load_amps",
            field=models.FloatField(blank=True, null=True, verbose_name="load (MW)"),
        ),
    ]
