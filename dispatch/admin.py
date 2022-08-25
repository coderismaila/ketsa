from django.contrib import admin
from dispatch.models import ForcedOutage, LoadReading


class LoadReadingConfig(admin.ModelAdmin):
    list_display = ("station", "feeder", "hour", "load_amps", "status", "status", "date")
    list_filter = ("date", "feeder__name")
    ordering = ("date",)

    def feeder(self, obj):
        return obj.feeder.name

    def station(self, obj):
        return obj.feeder.power_transformer.station.name

    def date(self, obj):
        return obj.date.date()

    def hour(self, obj):
        return str(obj.date.hour).zfill(2)


class ForcedOutageAdminConfig(admin.ModelAdmin):
    list_display = ("feeder", "relay_indicator", "time_out", "time_in", "induced_by", "remark")
    list_filter = ("feeder", "relay_indicator", "time_out", "induced_by")


admin.site.register(LoadReading, LoadReadingConfig)
admin.site.register(ForcedOutage, ForcedOutageAdminConfig)
