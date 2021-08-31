import datetime

from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone

from common.functions import date_calc
from properties.models import (
    PropertyFees,
    Instruction,
    Reduction,
    Valuation,
    ExchangeMoveSales,
    ExchangeMoveLettings,
)
from users.models import Profile


def sort_and_direction(sort, direction):
    """
    Returns the values to sort the overview stats.
    """

    data = {}

    dict = {
        "valuations": "valuation_count",
        "instructions": "instruction_count",
        "reductions": "reduction_count",
        "new_business": "new_business_sum",
        "exchanges": "exchange_count",
    }

    if direction == "desc":
        data["direction"] = True
    else:
        data["direction"] = False

    data["sort"] = dict[sort]

    return data


@otp_required
@login_required
def overview(request):
    """
    A view to return an overview
    """

    filter = "current_quarter"
    link_to_employee = "propertyprocess__employee"
    employee = "propertyprocess__employee__id"
    exchange_link_to_employee = "exchange__propertyprocess__employee"
    exchange_employee = "exchange__propertyprocess__employee__id"
    sort = None
    direction = None

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if "sort" in request.GET:
        sort = request.GET.get("sort")

    if "direction" in request.GET:
        direction = request.GET.get("direction")

    if filter == "current_quarter":
        date_calc_data = date_calc(timezone.now(), filter)
        start_date = date_calc_data["start_date"]
        end_date = date_calc_data["end_date"]
    else:
        start_date = request.GET.get("start-date")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        end_date = request.GET.get("end-date")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    valuations = (
        Valuation.objects.values("valuer")
        .exclude(active=False)
        .annotate(valuation_count=Count(link_to_employee))
        .filter(
            date__range=[start_date, end_date],
        )
        .order_by("-valuation_count")
    )

    instructions = (
        Instruction.objects.values(employee)
        .exclude(active=False)
        .annotate(instruction_count=Count(link_to_employee))
        .filter(
            date__range=[start_date, end_date],
        )
        .order_by("-instruction_count")
    )

    reductions = (
        Reduction.objects.values(employee)
        .annotate(reduction_count=Count(link_to_employee))
        .filter(
            date__range=[start_date, end_date],
        )
        .order_by("-reduction_count")
    )

    exchanges_sales = (
        ExchangeMoveSales.objects.values(exchange_employee)
        .annotate(sales_count=Count(exchange_link_to_employee))
        .filter(
            exchange_date__range=[start_date, end_date],
        )
        .order_by("-sales_count")
    )

    exchanges_lettings = (
        ExchangeMoveLettings.objects.values(exchange_employee)
        .annotate(lettings_count=Count(exchange_link_to_employee))
        .filter(
            move_in_date__range=[start_date, end_date],
        )
        .order_by("-lettings_count")
    )

    new_business = (
        PropertyFees.objects.values(employee)
        .annotate(new_business_sum=Sum("new_business"))
        .filter(
            date__range=[start_date, end_date],
            active=True,
            show_all=True,
        )
        .order_by("-new_business_sum")
    )

    for instance in instructions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

    for instance in reductions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

    for instance in new_business:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

    for instance in exchanges_sales:
        instance["employee_id"] = instance[
            "exchange__propertyprocess__employee__id"
        ]
        del instance["exchange__propertyprocess__employee__id"]

    for instance in exchanges_lettings:
        instance["employee_id"] = instance[
            "exchange__propertyprocess__employee__id"
        ]
        del instance["exchange__propertyprocess__employee__id"]

    exchanges = []

    for sales_instance in exchanges_sales:
        for lettings_instance in exchanges_lettings:
            if (
                sales_instance["employee_id"]
                == lettings_instance["employee_id"]
            ):
                exchange = {}
                exchange["employee_id"] = sales_instance["employee_id"]
                count = (
                    sales_instance["sales_count"]
                    + lettings_instance["lettings_count"]
                )
                exchange["exchange_count"] = count

                exchanges.append(exchange)

    employees = Profile.objects.all()

    overview_list = []
    stats = []

    for instance in employees:
        employee_dict = {}
        employee_dict["id"] = instance.id
        employee_dict["name"] = instance.user.get_full_name()
        employee_dict["employee_targets"] = instance.employee_targets
        employee_dict["active"] = instance.user.is_active

        employee_dict["valuation_count"] = 0
        employee_dict["instruction_count"] = 0
        employee_dict["reduction_count"] = 0
        employee_dict["new_business_sum"] = 0
        employee_dict["exchange_count"] = 0

        overview_list.append(employee_dict)

    for instance in overview_list:
        for valuation_instance in valuations:
            if instance["id"] == valuation_instance["valuer"]:
                instance["valuation_count"] = valuation_instance[
                    "valuation_count"
                ]
        for instruction_instance in instructions:
            if instance["id"] == instruction_instance["employee_id"]:
                instance["instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
        for reduction_instance in reductions:
            if instance["id"] == reduction_instance["employee_id"]:
                instance["reduction_count"] = reduction_instance[
                    "reduction_count"
                ]
        for new_business_instance in new_business:
            if instance["id"] == new_business_instance["employee_id"]:
                instance["new_business_sum"] = new_business_instance[
                    "new_business_sum"
                ]
        for exchange_instance in exchanges:
            if instance["id"] == exchange_instance["employee_id"]:
                instance["exchange_count"] = exchange_instance[
                    "exchange_count"
                ]

        if (
            instance["valuation_count"] == 0
            and instance["instruction_count"] == 0
            and instance["reduction_count"] == 0
            and instance["new_business_sum"] == 0
            and instance["exchange_count"] == 0
        ):
            pass
        else:
            stats.append(instance)

    if sort is not None and direction is not None:
        s_and_d = sort_and_direction(sort, direction)

        stats = sorted(
            stats,
            key=lambda k: k[s_and_d["sort"]],
            reverse=s_and_d["direction"],
        )

    context = {
        "filter": filter,
        "start_date": start_date,
        "end_date": end_date,
        "sort": sort,
        "direction": direction,
        "stats": stats,
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

    date_calc_data = date_calc(timezone.now(), selected_filter)

    start_date = date_calc_data["start_date"]
    end_date = date_calc_data["end_date"]

    data["start_date"] = start_date
    data["end_date"] = end_date
    data["filter"] = selected_filter

    return JsonResponse(data)
