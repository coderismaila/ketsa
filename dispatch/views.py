from django.shortcuts import render
from django.forms import modelformset_factory
from datetime import datetime
import pytz

# from dispatch.forms import CreateLoadReadingForm
from core.models import Feeder
from dispatch.models import Grid, LoadReading
from dispatch.forms import GridForm


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

            # we dont want 00:00:00 to be associated with the next day so we
            # reset it to the previous day by substracting a second
            if hour == 0:
                hour = 23
                dt = datetime(year, month, day, hour, minute=59, second=59)
                return dt
            dt = datetime(year, month, day, hour)
            return dt
        except:
            return None
    return None


def load_reading_form(request):
    query_dict = request.GET
    qs = None
    dt = None
    go = None
    grid_form = GridForm()

    try:
        dt = parse_dt(query_dict.get("date"), query_dict.get("hour"))

        # check if date already in database
        date_exists = LoadReading.objects.filter(date=dt).count()
        if date_exists == 0:
            # initialize new load reading data for the particular date and hour
            feeders = Feeder.objects.all()
            for feeder in feeders:
                reading = LoadReading.objects.create(date=dt, feeder=feeder, load_mw=0)
                reading.save()
        go = Grid.objects.get_or_create(date=dt)
        grid_form = GridForm(instance=go[0])
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
    formset = LoadReadingFormset(queryset=qs)

    if request.method == "POST":
        if request.POST.get("action") == "load_reading":
            formset = LoadReadingFormset(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
        if request.POST.get("action") == "grid_reading":
            # grid form
            grid_form = GridForm(request.POST, instance=go[0])
            if grid_form.is_valid():
                grid_form.save()

    return render(
        request,
        "dispatch/load_reading_form.html",
        {
            "formset": formset,
            "grid_form": grid_form,
            "selected_date": dt,
        },
    )


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
