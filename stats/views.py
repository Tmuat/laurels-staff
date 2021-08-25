import datetime

from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone

from common.functions import quarter_and_year_calc, date_calc
from properties.models import (
    Offer,
    PropertyFees,
    Instruction,
    Reduction,
    Valuation,
)

# def person_valuations():

#     link_to_employee = "propertyprocess__employee"

#     return


@otp_required
@login_required
def overview(request):
    """A view to return an overview"""

    """
    Current Quarter
    Last Quarter
    Year To Date
    Previous Year
    All Time
    """

    filter = "current_quarter"
    link_to_employee = "propertyprocess__employee"

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if filter == "current_quarter":
        date_calc_data = date_calc(timezone.now(), filter)
        start_date = date_calc_data["start_date"]
        end_date = date_calc_data["end_date"]
    else:
        start_date = request.GET.get("start-date")
        start_date = (
            datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        )

        end_date = request.GET.get("end-date")
        end_date = (
            datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        )

    valuations = (
        Valuation.objects.values("valuer")
        .exclude(active=False)
        .annotate(valuation_count=Count(link_to_employee))
        .filter(
            date__range=[start_date, end_date],
            propertyprocess__employee__employee_targets=True,
            propertyprocess__employee__user__is_active=True,
        )
        .order_by("-valuation_count")
    )

    context = {
        "filter": filter,
        "start_date": start_date,
        "end_date": end_date
    }

    return render(request, "stats/overview.html", context)


@otp_required
@login_required
def more_filters(request):
    """
    A view to return an ajax response with extra filters for dates
    """

    data = dict()

    data["html_modal"] = render_to_string(
        "stats/includes/date_form_modal.html",
        request=request,
    )
    return JsonResponse(data)


def quick_filter_conversion(request):
    """
    Converts quick filter to start and end dates.
    """

    data = dict()

    if "filter" in request.GET:
        selected_filter = request.GET.get("filter")

    # if selected_filter == "current_quarter":
    date_calc_data = date_calc(timezone.now(), selected_filter)

    start_date = date_calc_data["start_date"]
    end_date = date_calc_data["end_date"]

    data["start_date"] = start_date
    data["end_date"] = end_date
    data["filter"] = selected_filter

    return JsonResponse(data)
