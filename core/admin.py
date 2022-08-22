from django.contrib import admin

from core import models


class AreaOfficeAdminConfig(admin.ModelAdmin):
    list_display = ("name", "technical_manager")
    ordering = ("name",)


class BandAdminConfig(admin.ModelAdmin):
    list_display = ("name", "hos")
    ordering = ("name",)


class FeederAdminConfig(admin.ModelAdmin):
    list_display = (
        "station",
        "name",
        "band",
        "area_office",
        "peak_load_mw",
        "average_load_mw",
        "route_length",
    )
    list_filter = (
        "name",
        "area_office",
        "band",
    )

    def station(self, obj):
        return obj.power_transformer.station.name


admin.site.register(models.AreaOffice, AreaOfficeAdminConfig)
admin.site.register(models.Station)
admin.site.register(models.PowerTransformer)
admin.site.register(models.Band, BandAdminConfig)
admin.site.register(models.Feeder, FeederAdminConfig)
