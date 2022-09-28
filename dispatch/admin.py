from django.contrib import admin
from dispatch.models import ForcedOutage, Grid, LoadReading
from mixins.export_csv_mixins import ExportCsvMixin


class LoadReadingConfig(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("station", "feeder", "hour", "load_mw", "status", "date")
    list_filter = ("date", "feeder__name")
    ordering = ("date",)
    actions = ["export_as_csv"]

    def feeder(self, obj):
        return obj.feeder.name

    def station(self, obj):
        return obj.feeder.power_transformer.station.name

    def date(self, obj):
        return obj.date.date()

    def hour(self, obj):
        return str(obj.date.hour).zfill(2)


# class LoadAllocationAndGeneration()


class ForcedOutageAdminConfig(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("feeder", "relay_indicator", "time_out", "time_in", "induced_by", "remark")
    list_filter = ("feeder", "relay_indicator", "time_out", "induced_by")
    actions = ["export_as_csv"]


class GridAdminConfig(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("date", "generation_mw", "allocation_mw")
    list_filter = ("date",)
    actions = ["export_as_csv"]


admin.site.register(LoadReading, LoadReadingConfig)
admin.site.register(ForcedOutage, ForcedOutageAdminConfig)
admin.site.register(Grid, GridAdminConfig)
