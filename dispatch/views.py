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
            dt = datetime(year, month, day, hour).astimezone()
            return dt
        except:
            return None
    return None


def load_reading_form(request):
    query_dict = request.GET
    qs = None
    dt = None

    try:
        dt = parse_dt(query_dict.get("date"), query_dict.get("hour"))

        # check if date already in database
        date_exists = LoadReading.objects.filter(date=dt).count()
        if date_exists == 0:
            # initialize new load reading data for the particular date and hour
            feeders = Feeder.objects.all()
            for feeder in feeders:
                reading = LoadReading.objects.create(
                    date=dt, feeder=feeder, load_mw=0, allocation_mw=0, generation_mw=0
                )
                reading.save()
    except:
        qs = None

    # get load reading for the datetime
    qs = LoadReading.objects.filter(date=dt).all()

    # create formset for load reading
    LoadReadingFormset = modelformset_factory(
        LoadReading,
        fields=("date", "feeder", "load_mw", "status"),
        extra=0,
    )
    # initialize formset

    if request.method == "POST":
        formset = LoadReadingFormset(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()

    else:
        formset = LoadReadingFormset(queryset=qs)

    return render(request, "dispatch/load_reading_form.html", {"formset": formset, "selected_date": dt})


def load_reading_table(request):
    query_dict = request.GET
    qs = None
    dt = None
    feeders = None

    try:
        dt = parse_dt(query_dict.get("date"), "00:00")

        # get load reading for the datetime
        qs = (
            LoadReading.objects.filter(date__day=dt.day, date__month=dt.month, date__year=dt.year)
            .all()
            .order_by("date")
        )
        print("qs")
        print(qs.count())
        feeders = Feeder.objects.all()
    except:
        qs = None

    return render(
        request,
        "dispatch/load_reading_table.html",
        {
            "objects": qs,
            "fdrs": feeders,
            "selected_date": dt,
        },
    )
