# Generated by Django 3.2.15 on 2022-09-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0010_alter_grid_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grid',
            name='allocation_mw',
            field=models.FloatField(verbose_name='allocation (mw)'),
        ),
        migrations.AlterField(
            model_name='grid',
            name='generation_mw',
            field=models.FloatField(verbose_name='generation (mw)'),
        ),
    ]
