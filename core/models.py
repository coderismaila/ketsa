from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


class AreaOffice(models.Model):
    name = models.CharField(
        _("area office"),
        max_length=25,
        blank=False,
        null=False,
        unique=True,
        error_messages={
            "unique": _("name already assigned to another area office"),
        },
    )
    code = models.CharField(
        _("code"),
        max_length=5,
        unique=True,
        help_text=_("Required. 3 characters uniqe code"),
        error_messages={
            "unique": _("Code already assigned to another area office"),
        },
    )
    technical_manager = models.OneToOneField(CustomUser, unique=True, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Station(models.Model):
    DISTRIBUTION = "DR"
    TRANSMISSION = "TR"
    STATION_TYPE = [
        (DISTRIBUTION, "Distribution"),
        (TRANSMISSION, "Transmission"),
    ]

    name = models.CharField(
        _("name"),
        max_length=75,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
    )
    capacity_kva = models.PositiveIntegerField(_("capacity (kva)"), null=True, blank=True)
    type = models.CharField(max_length=2, choices=STATION_TYPE, default=DISTRIBUTION)

    def __str__(self):
        return self.name


class PowerTransformer(models.Model):
    HIGH_VOLTAGE = "330/132KV"
    MEDIUM_VOLTAGE = "132/33KV"
    LOW_VOLTAGE = "33/11KV"
    VOLTAGE_RATING = [
        (HIGH_VOLTAGE, "330/132KV"),
        (MEDIUM_VOLTAGE, "132/33KV"),
        (LOW_VOLTAGE, "33/11KV"),
    ]
    name = models.CharField(_("name"), max_length=50)
    capacity_kva = models.PositiveIntegerField(
        _("capacity (kva)"),
        null=False,
        blank=False,
    )
    voltageRating = models.CharField(
        max_length=9,
        choices=VOLTAGE_RATING,
        default=LOW_VOLTAGE,
    )
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " - " + str(self.capacity_kva / 1000) + "MVA - " + self.station.name


class Band(models.Model):
    name = models.CharField(_("feeder band"), max_length=1, unique=True, blank=False, null=False)
    description = models.CharField(_("band description"), max_length=1, blank=True, null=True)
    hos = models.PositiveSmallIntegerField(_("hours of supply"), null=False, blank=False)

    def __str__(self):
        return self.name


class Feeder(models.Model):
    name = models.CharField(_("feeder name"), max_length=50, unique=True, db_index=True, blank=False, null=False)
    band = models.ForeignKey(Band, unique=False, on_delete=models.SET_NULL, null=True, blank=True)
    peak_load_mw = models.FloatField(_("peak load (mw)"), blank=True, null=True)
    average_load_mw = models.FloatField(_("average load (mw)"), blank=True, null=True)
    route_length = models.FloatField(_("route length"), null=True, blank=True)
    kaedco_code = models.CharField(_("kaedco code"), max_length=4, unique=True, null=False, blank=False)
    nerc_code = models.CharField(_("nerc code"), max_length=4, unique=True, null=False, blank=False)
    power_transformer = models.ForeignKey(PowerTransformer, on_delete=models.SET_NULL, null=True)
    area_office = models.ForeignKey(AreaOffice, on_delete=models.SET_NULL, null=True)
    voltage_level = models.CharField(_("voltage level"), max_length=4, choices=[("11", "11KV"), ("33", "33KV")])

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(_("phone number"), max_length=14, null=True, blank=True)
    personal_email = models.EmailField(_("personal email"), unique=True, null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=1, choices=[("M", "Male"), ("F", "Female")])
    birth_date = models.DateField(_("date of birth"), null=True, blank=True)
    area_office = models.ForeignKey(AreaOffice, on_delete=models.SET_NULL, null=True, blank=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)
    # job_role
    # designation
    # birth_date
    # area_office
    # station
    # adress_line_1
    # adress_line_2
    # city
    # state
    # state_of_origin
