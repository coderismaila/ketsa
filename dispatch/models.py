from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Feeder


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
    load_amps = models.FloatField(_("load (A)"), blank=True, null=True)
    status = models.CharField(_("feeder status"), max_length=3, choices=STATUS, blank=True, null=True)

    # def __str__(self):
    #     return self.feeder.name
