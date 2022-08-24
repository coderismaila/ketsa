from django.shortcuts import render
from django.forms import modelformset_factory
from datetime import datetime
import pytz

# from dispatch.forms import CreateLoadReadingForm
from core.models import Feeder
from dispatch.models import LoadReading


def parse_dt(date, time):
    if date is not None and time is not None:
        year = None
        month = None
        day = None
        hour = None

        try:
            year = int(date.split("-")[0])
            month = int(date.split("-")[1])
            day = int(date.split("-")[-1])
            hour = int(time.split(":")[0])
            dt = datetime(year, month, day, hour).astimezone(pytz.UTC)
            return dt
        except:
            return None
    return None


def load_reading(request):
    query_dict = request.GET
    qs = None
    dt = None

    try:
        dt = parse_dt(query_dict.get("date"), query_dict.get("hour"))

        # check if date already in database
        date_exists = LoadReading.objects.filter(date=dt).count()
        print(date_exists)
        if date_exists == 0:
            # initialize new load reading data for the particular date and hour
            feeders = Feeder.objects.all()
            for feeder in feeders:
                reading = LoadReading.objects.create(date=dt, feeder=feeder, load_amps=0)
                reading.save()
    except:
        qs = None

    # get load reading for the datetime
    qs = LoadReading.objects.filter(date=dt).all()

    # create formset for load reading
    LoadReadingFormset = modelformset_factory(
        LoadReading,
        fields=("date", "feeder", "load_amps", "status"),
        extra=0,
    )
    # initialize formset

    if request.method == "POST":
        print("Saving form...")
        formset = LoadReadingFormset(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
        print("Form saved!")

    else:
        formset = LoadReadingFormset(queryset=qs)

    return render(request, "dispatch/load_reading.html", {"formset": formset})


def create_load_reading(request):
    LoadReadingFormset = modelformset_factory(
        LoadReading,
        fields=("date", "feeder", "load_amps", "status"),
        extra=0,
    )

    formset = LoadReadingFormset()

    return render(request, "dispatch/load_reading_form.html", {"formset": formset})
