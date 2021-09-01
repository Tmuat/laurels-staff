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
        "exchanges": "exchange_sum",
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

    exchanges_sales = ExchangeMoveSales.objects.filter(
        exchange_date__range=[start_date, end_date],
    ).order_by("-exchange_date")

    exchanges_lettings = ExchangeMoveLettings.objects.filter(
        move_in_date__range=[start_date, end_date],
    ).order_by("-move_in_date")

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
        employee_dict["exchange_sum"] = 0

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

        for exchanges_sales_instance in exchanges_sales:
            if instance["id"] == exchanges_sales_instance.exchange.propertyprocess.employee.id:
                instance["exchange_sum"] += exchanges_sales_instance.exchange.propertyprocess.property_fees.last().new_business

        for exchanges_lettings_instance in exchanges_lettings:
            if instance["id"] == exchanges_lettings_instance.exchange.propertyprocess.employee.id:
                instance["exchange_sum"] += exchanges_lettings_instance.exchange.propertyprocess.property_fees.last().new_business

        if (
            instance["valuation_count"] == 0
            and instance["instruction_count"] == 0
            and instance["reduction_count"] == 0
            and instance["new_business_sum"] == 0
            and instance["exchange_sum"] == 0
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


@otp_required
@login_required
def employee_exchanges(request, profile_id, start_date, end_date):
    """
    An AJAX view to return all exchanges in a given date range
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    start_date = datetime.datetime.strptime(start_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )
    end_date = datetime.datetime.strptime(end_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )

    exchanges_sales = ExchangeMoveSales.objects.filter(
        exchange__propertyprocess__employee__id=profile_id,
        exchange_date__range=[start_date, end_date],
    ).order_by("-exchange_date")

    exchanges_lettings = ExchangeMoveLettings.objects.filter(
        exchange__propertyprocess__employee__id=profile_id,
        move_in_date__range=[start_date, end_date],
    ).order_by("-move_in_date")

    exchanges = []

    for instance in exchanges_sales:
        exchange_dict = {}
        exchange_dict["id"] = instance.id
        exchange_dict["address"] = instance.exchange.propertyprocess
        exchange_dict["sector"] = instance.exchange.propertyprocess.sector
        exchange_dict["property_proccess"] = instance.exchange.propertyprocess.id
        exchange_dict["date"] = instance.exchange_date
        exchange_dict["comp_date"] = instance.completion_date
        exchange_dict["sum"] = instance.exchange.propertyprocess.property_fees.last().new_business
        exchange_dict["fee"] = instance.exchange.propertyprocess.property_fees.last().fee
        exchange_dict["final_price"] = instance.exchange.propertyprocess.property_fees.last().price

        exchanges.append(exchange_dict)

    for instance in exchanges_lettings:
        exchange_dict = {}
        exchange_dict["id"] = instance.id
        exchange_dict["address"] = instance.exchange.propertyprocess
        exchange_dict["sector"] = instance.exchange.propertyprocess.sector
        exchange_dict["property_proccess"] = instance.exchange.propertyprocess.id
        exchange_dict["date"] = instance.move_in_date
        exchange_dict["sum"] = instance.exchange.propertyprocess.property_fees.last().new_business
        exchange_dict["fee"] = instance.exchange.propertyprocess.property_fees.last().fee
        exchange_dict["final_price"] = instance.exchange.propertyprocess.property_fees.last().price

        exchanges.append(exchange_dict)

    exchanges = sorted(
            exchanges,
            key=lambda k: k["date"],
            reverse=True,
        )

    context = {"exchanges": exchanges, "user": user}

    data["html_modal"] = render_to_string(
        "stats/includes/exchange.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def employee_new_business(request, profile_id, start_date, end_date):
    """
    An AJAX view to return all new_business in a given date range
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    start_date = datetime.datetime.strptime(start_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )
    end_date = datetime.datetime.strptime(end_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )

    new_business = (
        PropertyFees.objects.filter(
            propertyprocess__employee__id=profile_id,
            date__range=[start_date, end_date],
            active=True,
            show_all=True,
        )
        .order_by("-date")
    )

    context = {"new_business": new_business, "user": user}

    data["html_modal"] = render_to_string(
        "stats/includes/new_business.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def employee_reductions(request, profile_id, start_date, end_date):
    """
    An AJAX view to return all reductions in a given date range
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    start_date = datetime.datetime.strptime(start_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )
    end_date = datetime.datetime.strptime(end_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )

    reductions = (
        Reduction.objects.filter(
            propertyprocess__employee__id=profile_id,
            date__range=[start_date, end_date],
        )
        .order_by("-date")
    )

    context = {"reductions": reductions, "user": user}

    data["html_modal"] = render_to_string(
        "stats/includes/reductions.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def employee_instructions(request, profile_id, start_date, end_date):
    """
    An AJAX view to return all instructions in a given date range
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    start_date = datetime.datetime.strptime(start_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )
    end_date = datetime.datetime.strptime(end_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )

    instructions = (
        Instruction.objects.filter(
            propertyprocess__employee__id=profile_id,
            date__range=[start_date, end_date],
        )
        .exclude(active=False)
        .order_by("-date")
    )

    context = {"instructions": instructions, "user": user}

    data["html_modal"] = render_to_string(
        "stats/includes/instructions.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def employee_valuations(request, profile_id, start_date, end_date):
    """
    An AJAX view to return all valuations in a given date range
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    start_date = datetime.datetime.strptime(start_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )
    end_date = datetime.datetime.strptime(end_date, "%d-%m-%y").strftime(
        "%Y-%m-%d"
    )

    valuations = (
        Valuation.objects.filter(
            valuer=profile_id,
            date__range=[start_date, end_date],
        )
        .exclude(active=False)
        .order_by("-date")
    )

    context = {"valuations": valuations, "user": user}

    data["html_modal"] = render_to_string(
        "stats/includes/valuations.html",
        context,
        request=request,
    )

    return JsonResponse(data)