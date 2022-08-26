from django.shortcuts import render
from core.models import Feeder
from django.db.models import Count, Sum, Avg
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from datetime import datetime

from dispatch.models import LoadReading

# px.defaults.width = 600
# px.defaults.height = 400


def home(request):
    return render(request, "core/base.html")


def dashboard(request):
    today = datetime.today()

    load_reading_qs = (
        LoadReading.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)
        .values("date")
        .order_by("date")
    )

    load_qs = list(load_reading_qs.annotate(sum=Sum("load_mw")))
    allocation_qs = list(load_reading_qs.annotate(avg=Avg("allocation_mw")))
    load_qs.append(allocation_qs)
    print(load_qs)

    area_offices = []
    counts = []
    qs = Feeder.objects.values("area_office__name").annotate(count=Count("name"))

    for feeder in qs:
        area_offices.append(feeder["area_office__name"])
        counts.append(feeder["count"])

    df = pd.DataFrame(list(zip(area_offices, counts)), columns=["area office", "feeder count"])

    fig = px.bar(df, y="area office", x="feeder count", text_auto=".1s", orientation="h")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color="green")
    fig.update_layout({"plot_bgcolor": "white", "paper_bgcolor": "white"})
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    # fig.update_layout(width=506, height=384)
    bar_chart = plot(fig, output_type="div")
    return render(request, "core/dashboard.html", {"bar_chart": bar_chart})
