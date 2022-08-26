from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Feeder


class Grid(models.Model):
    date = models.DateTimeField(_("date"), null=False, blank=False)
    allocation_mw = models.FloatField(_("allocation (mw"), null=False, blank=False)
    generation_mw = models.FloatField(_("generation (mw"), null=False, blank=False)
    status = models.CharField(
        _("grid status"),
        max_length=10,
        choices=[
            ("IN CIRCUIT", "In Circuit"),
            ("BLACKOUT", "Blackout"),
        ],
    )


class LoadReading(models.Model):
    LOAD_SHEDDING = "L/S"
    OUT_OF_SERVICE = "O/S"
    FREQUENCY_CONTROL = "F/C"
    SYSTEM_COLLAPSE = "S/C"
    FAULT = "O/F"
    PLANNED_OUTAGE = "P/O"
    IN_CIRCUIT = "IN"

    STATUS = [
        (LOAD_SHEDDING, "LOAD SHEDDING"),
        (OUT_OF_SERVICE, "OUT OF SERVICE"),
        (FREQUENCY_CONTROL, "FREQUENCY CONTROL"),
        (SYSTEM_COLLAPSE, "SYSTEM COLLAPSE"),
        (FAULT, "FAULT"),
        (PLANNED_OUTAGE, "PLANNED OUTAGE"),
        (IN_CIRCUIT, "IN CIRCUIT"),
    ]
    date = models.DateTimeField(_("date"), blank=False, null=False)
    feeder = models.ForeignKey(Feeder, on_delete=models.SET_NULL, null=True, blank=True, unique=False)
    load_mw = models.FloatField(_("load (MW)"), blank=True, null=True)

    status = models.CharField(_("feeder status"), max_length=3, choices=STATUS, blank=True, null=True)

    # def __str__(self):
    #     return self.feeder.name


class ForcedOutage(models.Model):
    OVERCURRENT = "O/C"
    EARTH_FAULT = "E/F"
    OVERCURRENT_AND_EARTH_FAULT = "O/C & E/F"
    OUT_OF_SERVICE = "O/S"
    FREQUENCY_CONTROL = "F/C"
    RELAY_INDICATOR = [
        (OVERCURRENT, "Over Current"),
        (EARTH_FAULT, "Earth Fault"),
        (OVERCURRENT_AND_EARTH_FAULT, "Over Current & Earth Fault"),
        (OUT_OF_SERVICE, "Out of Service"),
        (FREQUENCY_CONTROL, "Frequency Control"),
    ]
    feeder = models.ForeignKey(Feeder, on_delete=models.SET_NULL, null=True, blank=True)
    time_out = models.DateTimeField(_("time out"), blank=False, null=False)
    time_in = models.DateTimeField(_("time in"), blank=True, null=True)
    relay_indicator = models.CharField(_("relay indicator"), max_length=10, choices=RELAY_INDICATOR)
    induced_by = models.CharField(
        _("induced by"), max_length=10, choices=[("KAEDCO", "KAEDCO"), ("GRID", "GRID")], null=True, blank=True
    )
    remark = models.CharField(_("remark"), max_length=255, null=True, blank=True)
