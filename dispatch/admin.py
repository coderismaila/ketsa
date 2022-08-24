from django.contrib import admin
from dispatch.models import LoadReading


class LoadReadingConfig(admin.ModelAdmin):
    list_display = ("station", "feeder", "hour", "load_amps", "status", "status", "date")
    list_filter = ("date",)
    ordering = ("date",)

    def feeder(self, obj):
        return obj.feeder.name

    def station(self, obj):
        return obj.feeder.power_transformer.station.name

    def date(self, obj):
        return obj.date.date()

    def hour(self, obj):
        return str(obj.date.hour).zfill(2)


admin.site.register(LoadReading, LoadReadingConfig)
