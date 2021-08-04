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
def normal_by_person(request):
    """A view to return the stats page for normal stats by person"""

    """
    Current Quarter
    Last Quarter
    Year To Date
    Previous Year
    All Time
    """

    link_to_employee = "propertyprocess__employee"

    quarter_and_year = quarter_and_year_calc(timezone.now())

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]
    quarter = quarter_and_year["quarter"]
    company_year = quarter_and_year["company_year"]

    valuations = (
        Valuation.objects.values("valuer")
        .annotate(valuation_count=Count(link_to_employee))
        .filter(
            date__iso_year=year,
            date__month__gte=start_month,
            date__month__lte=end_month,
            propertyprocess__employee__employee_targets=True,
            propertyprocess__employee__user__is_active=True,
        )
        .order_by("-valuation_count")
    )

    context = {}

    return render(request, "stats/normal_by_person.html", context)


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

    return JsonResponse(data)
