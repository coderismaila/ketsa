from django.shortcuts import render
from core.models import Feeder
from django.db.models import Sum
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from datetime import datetime, timedelta

from dispatch.models import Grid, LoadReading

# px.defaults.margins = dict(l=0, r=0, t=50, b=50)
px.defaults.height = 320

hour_list = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "00",
]
hour_category = pd.api.types.CategoricalDtype(ordered=True, categories=hour_list)


def home(request):
    return render(request, "core/base.html")


def dashboard(request):
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    # get latest grid reading
    grid_reading = Grid.objects.all().order_by("date").last()

    # get total load across all feeders at current grid reading time
    current_load_reading = LoadReading.objects.filter(date=grid_reading.date).aggregate(load_mw=Sum("load_mw"))

    # get current load and grid reading for the day
    load_reading_qs = (
        LoadReading.objects.filter(
            date__year=grid_reading.date.year,
            date__month=grid_reading.date.month,
            date__day=grid_reading.date.day,
        )
        .all()
        .values("date", "load_mw")
    )

    # query for load center at grid date and hour
    load_center_qs = (
        LoadReading.objects.filter(date=grid_reading.date)
        .all()
        .values("date", "load_mw", "feeder__power_transformer__station__short_name")
    )

    # query for total load taken by area offices for current month
    area_office_qs = LoadReading.objects.filter(
        date__year=grid_reading.date.year, date__month=grid_reading.date.month
    ).values("date", "feeder__area_office__name", "load_mw")
    area_office_frame = pd.DataFrame(area_office_qs)
    area_office_frame = (
        area_office_frame.groupby("feeder__area_office__name")["load_mw"].sum().reset_index(name="load_taken_mw")
    )

    # query for load taken for the current month
    month_load_reading_qs = LoadReading.objects.filter(
        date__year=grid_reading.date.year, date__month=grid_reading.date.month
    ).values("date", "load_mw")
    month_load_reading_df = pd.DataFrame(month_load_reading_qs)
    month_load_reading_df["day"] = month_load_reading_df.date.dt.day

    month_load_reading_df = month_load_reading_df.groupby("day")["load_mw"].sum().reset_index(name="load_taken_mw")

    # get aggregate energy consumed by companywide for the month
    current_month_load = LoadReading.objects.filter(
        date__year=grid_reading.date.year, date__month=grid_reading.date.month
    ).aggregate(current_month_load_mw=Sum("load_mw"))

    grid_qs = grid_reading

    grid_qs = (
        Grid.objects.filter(
            date__year=grid_reading.date.year,
            date__month=grid_reading.date.month,
            date__day=grid_reading.date.day,
        )
        .all()
        .values("date", "allocation_mw")
    )

    load_reading_frame = pd.DataFrame(load_reading_qs)
    load_reading_frame_by_date = load_reading_frame.groupby("date")["load_mw"].sum().reset_index(name="load_taken_mw")

    load_center_frame = pd.DataFrame(load_center_qs)
    load_center_frame = (
        load_center_frame.groupby("feeder__power_transformer__station__short_name")["load_mw"]
        .sum()
        .reset_index(name="load_taken_mw")
    )
    load_center_frame.dropna(inplace=True, axis=1)

    grid_qs_frame = pd.DataFrame(grid_qs)

    merged_frame = load_reading_frame_by_date.merge(grid_qs_frame, how="left", on="date")

    merged_frame["hour"] = merged_frame.date.dt.hour

    # keep reading at midnight to previous day
    merged_frame.loc[merged_frame["date"].dt.minute == 59, "hour"] = 0

    merged_frame["hour"] = merged_frame.hour.astype(str)
    merged_frame["hour"] = merged_frame.hour.str.zfill(2)
    merged_frame["hour"] = merged_frame["hour"].astype(hour_category)

    merged_frame = pd.melt(
        merged_frame,
        id_vars="hour",
        value_vars=("load_taken_mw", "allocation_mw"),
        var_name="grid",
        value_name="load",
    )
    max_load = merged_frame.load.max() + 20
    fig = px.line(
        merged_frame,
        x="hour",
        y="load",
        color="grid",
        markers=True,
        range_y=[0, max_load],
    )

    # area_offices = []
    # counts = []
    # qs = Feeder.objects.values("area_office__name").annotate(count=Count("name"))

    # for feeder in qs:
    #     area_offices.append(feeder["area_office__name"])
    #     counts.append(feeder["count"])

    # df = pd.DataFrame(list(zip(area_offices, counts)), columns=["area office", "feeder count"])

    # fig = px.bar(df, y="area office", x="feeder count", text_auto=".1s", orientation="h")
    fig.update_layout({"plot_bgcolor": "white"})
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=50))
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Load (MW)")
    fig.update_layout(legend=dict(yanchor="bottom", y=0.0, xanchor="auto", x=0.0), legend_title="")
    line_chart = plot(fig, output_type="div")

    fig2 = px.bar(
        load_center_frame,
        y="load_taken_mw",
        x="feeder__power_transformer__station__short_name",
        text_auto=".1s",
        orientation="v",
        color_discrete_sequence=["#1cc88a" for _ in range(load_center_frame.shape[1] + 1)],
    )
    fig2.update_layout({"plot_bgcolor": "white"})
    fig2.update_layout(margin=dict(l=0, r=0, t=50, b=50))
    fig2.update_yaxes(title_text="")
    fig2.update_xaxes(title_text="Load (MW)")

    bar_chart = plot(fig2, output_type="div")

    # area office load for the day
    fig3 = px.bar(
        area_office_frame,
        y="load_taken_mw",
        x="feeder__area_office__name",
        text_auto=".1s",
        orientation="v",
        color_discrete_sequence=["#1cc88a" for _ in range(load_center_frame.shape[1] + 1)],
    )
    fig3.update_layout({"plot_bgcolor": "white"})
    fig3.update_layout(margin=dict(l=0, r=0, t=50, b=50))
    fig3.update_xaxes(title_text="")
    fig3.update_yaxes(title_text="Load (MW)")

    area_office_bar_chart = plot(fig3, output_type="div")

    # daily load taken for current month
    fig4 = px.area(
        month_load_reading_df,
        y="load_taken_mw",
        x="day",
        color_discrete_sequence=["#1cc88a" for _ in range(month_load_reading_df.shape[1] + 1)],
    )
    fig4.update_layout({"plot_bgcolor": "white"})
    fig4.update_layout(margin=dict(l=0, r=0, t=50, b=50))
    fig4.update_xaxes(title_text="")
    fig4.update_yaxes(title_text="Load (MW)")

    daily_load_bar_chart = plot(fig4, output_type="div")

    print(current_month_load)

    return render(
        request,
        "core/dashboard.html",
        {
            "line_chart": line_chart,
            "bar_chart": bar_chart,
            "area_office_bar_chart": area_office_bar_chart,
            "daily_load_bar_chart": daily_load_bar_chart,
            "generation": grid_reading.generation_mw,
            "allocation": grid_reading.allocation_mw,
            "load_mw": current_load_reading,
            "current_month_load_mw": current_month_load["current_month_load_mw"] / 1000,
            "grid_datetime": grid_reading.date,
        },
    )
