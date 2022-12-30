import datetime
import xlwt

from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg, F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone

from common.decorators import director_required
from common.functions import date_calc, calculate_quarter_and_year
from properties.models import (
    PropertyProcess,
    PropertyFees,
    Instruction,
    Reduction,
    Valuation,
    ExchangeMoveSales,
    ExchangeMoveLettings,
)
from regionandhub.models import Hub
from users.models import Profile, UserTargets


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
        "inst_fee": "instruction_fee_avg",
        "lettings_inst_fee": "lettings_instruction_fee_avg",
        "inst_price": "instruction_list_price_avg",
        "lettings_instructions": "lettings_instruction_count",
        "lettings_inst_price": "lettings_instruction_list_price_avg",
        "val_inst": "val_to_inst",
        "reduced": "reduction_val",
        "inst_to_exch": "inst_to_exchange",
        "sales_weeks": "sales_weeks",
        "lettings_weeks": "lettings_weeks",
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
    hub = None
    sort = None
    direction = None

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if "hub" in request.GET:
        hub = request.GET.get("hub")

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

        if hub:
            for hub_instance in instance.hub.all():
                if hub == hub_instance.slug:
                    overview_list.append(employee_dict)
        else:
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
            if (
                instance["id"]
                == exchanges_sales_instance.exchange.propertyprocess.employee.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_sales_instance.exchange.propertyprocess.property_fees_master.new_business
                )

        for exchanges_lettings_instance in exchanges_lettings:
            if (
                instance["id"]
                == exchanges_lettings_instance.exchange.propertyprocess.employee.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_lettings_instance.exchange.propertyprocess.property_fees_master.new_business
                )

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
        "hub": hub,
        "sort": sort,
        "direction": direction,
        "stats": stats,
    }

    return render(request, "stats/overview.html", context)


@otp_required
@login_required
def hub_overview(request):
    """
    A view to return a hub overview & total company
    """

    filter = "current_quarter"
    link_to_hub = "propertyprocess__hub"
    hub = "propertyprocess__hub__id"
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

    all_valuations = Valuation.objects.exclude(active=False).filter(
        date__range=[start_date, end_date],
    )

    valuations = (
        all_valuations.values(hub)
        .annotate(valuation_count=Count(link_to_hub))
        .order_by("-valuation_count")
    )

    all_instructions = Instruction.objects.exclude(active=False).filter(
        date__range=[start_date, end_date],
    )

    instructions = (
        all_instructions.values(hub)
        .annotate(instruction_count=Count(link_to_hub))
        .order_by("-instruction_count")
    )

    all_reductions = Reduction.objects.filter(
        date__range=[start_date, end_date],
    )

    reductions = (
        all_reductions.values(hub)
        .annotate(reduction_count=Count(link_to_hub))
        .order_by("-reduction_count")
    )

    all_exchanges_sales = ExchangeMoveSales.objects.filter(
        exchange_date__range=[start_date, end_date],
    )

    exchanges_sales = all_exchanges_sales.order_by("-exchange_date")

    all_exchanges_lettings = ExchangeMoveLettings.objects.filter(
        move_in_date__range=[start_date, end_date],
    )

    exchanges_lettings = all_exchanges_lettings.order_by("-move_in_date")

    all_new_business = (
        PropertyFees.objects.exclude(active=False)
        .exclude(show_all=False)
        .filter(
            date__range=[start_date, end_date],
        )
    )

    new_business = (
        all_new_business.values(hub)
        .annotate(new_business_sum=Sum("new_business"))
        .order_by("-new_business_sum")
    )

    for instance in valuations:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in instructions:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in reductions:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in new_business:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    hubs = Hub.objects.filter(is_active=True)

    overview_list = []
    stats = []
    total = {
        "valuation_count": len(all_valuations),
        "instruction_count": len(all_instructions),
        "reduction_count": len(all_reductions),
        "new_business_sum": 0,
        "exchange_sum": 0,
    }

    for instance in hubs:
        hub_dict = {}
        hub_dict["id"] = instance.id
        hub_dict["hub_name"] = instance.hub_name

        hub_dict["valuation_count"] = 0
        hub_dict["instruction_count"] = 0
        hub_dict["reduction_count"] = 0
        hub_dict["new_business_sum"] = 0
        hub_dict["exchange_sum"] = 0

        overview_list.append(hub_dict)

    for instance in overview_list:
        for valuation_instance in valuations:
            if instance["id"] == valuation_instance["hub_id"]:
                instance["valuation_count"] = valuation_instance[
                    "valuation_count"
                ]
        for instruction_instance in instructions:
            if instance["id"] == instruction_instance["hub_id"]:
                instance["instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
        for reduction_instance in reductions:
            if instance["id"] == reduction_instance["hub_id"]:
                instance["reduction_count"] = reduction_instance[
                    "reduction_count"
                ]
        for new_business_instance in new_business:
            if instance["id"] == new_business_instance["hub_id"]:
                instance["new_business_sum"] = new_business_instance[
                    "new_business_sum"
                ]

        for exchanges_sales_instance in exchanges_sales:
            if (
                instance["id"]
                == exchanges_sales_instance.exchange.propertyprocess.hub.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_sales_instance.exchange.propertyprocess.property_fees_master.new_business
                )

        for exchanges_lettings_instance in exchanges_lettings:
            if (
                instance["id"]
                == exchanges_lettings_instance.exchange.propertyprocess.hub.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_lettings_instance.exchange.propertyprocess.property_fees_master.new_business
                )

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

    for instance in all_new_business:
        total["new_business_sum"] += instance.new_business

    for instance in exchanges_sales:
        total[
            "exchange_sum"
        ] += (
            instance.exchange.propertyprocess.property_fees_master.new_business
        )

    for instance in exchanges_lettings:
        total[
            "exchange_sum"
        ] += (
            instance.exchange.propertyprocess.property_fees_master.new_business
        )

    context = {
        "filter": filter,
        "start_date": start_date,
        "end_date": end_date,
        "sort": sort,
        "direction": direction,
        "stats": stats,
        "total": total,
    }

    return render(request, "stats/hub_overview.html", context)


@otp_required
@login_required
def extra_stats(request):
    """
    A view to return extra stats
    """

    filter = "current_quarter"
    link_to_employee = "propertyprocess__employee"
    employee = "propertyprocess__employee__id"
    hub = None
    sort = None
    direction = None

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if "hub" in request.GET:
        hub = request.GET.get("hub")

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

    all_valuations = Valuation.objects.exclude(active=False).filter(
        date__range=[start_date, end_date],
    )

    valuations = (
        all_valuations.values(employee)
        .annotate(valuation_count=Count(link_to_employee))
        .order_by("-valuation_count")
    )

    all_instructions = Instruction.objects.exclude(active=False).filter(
        date__range=[start_date, end_date],
    )

    instruction_reductions = all_instructions.annotate(
        reduced=Count("propertyprocess__reduction")
    )

    instructions = (
        all_instructions.values(employee)
        .annotate(instruction_count=Count(link_to_employee))
        .order_by("-instruction_count")
    )

    sales_instructions = (
        all_instructions.filter(
            propertyprocess__sector=PropertyProcess.SALES,
        )
        .values(employee)
        .annotate(instruction_fee_avg=Avg("fee_agreed"))
        .annotate(instruction_count=Count(link_to_employee))
        .annotate(instruction_list_price_avg=Avg("listing_price"))
        .order_by("-instruction_fee_avg")
    )

    lettings_instructions = (
        all_instructions.filter(
            propertyprocess__sector=PropertyProcess.LETTINGS,
        )
        .values(employee)
        .annotate(instruction_fee_avg=Avg("fee_agreed"))
        .annotate(instruction_count=Count(link_to_employee))
        .annotate(instruction_list_price_avg=Avg("listing_price"))
        .order_by("-instruction_fee_avg")
    )

    exchanges_sales = ExchangeMoveSales.objects.filter(
        exchange_date__range=[start_date, end_date],
    ).order_by("-exchange_date")

    exchanges_lettings = ExchangeMoveLettings.objects.filter(
        move_in_date__range=[start_date, end_date],
    ).order_by("-move_in_date")

    for instance in instructions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

    for instance in sales_instructions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

    for instance in lettings_instructions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

    for instance in valuations:
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
        employee_dict["val_to_inst"] = 0
        employee_dict["reduction_val"] = 0
        employee_dict["instruction_count"] = 0
        employee_dict["total_instruction_count"] = 0
        employee_dict["instruction_fee_avg"] = 0
        employee_dict["instruction_list_price_avg"] = 0
        employee_dict["lettings_instruction_count"] = 0
        employee_dict["lettings_instruction_fee_avg"] = 0
        employee_dict["lettings_instruction_list_price_avg"] = 0
        employee_dict["reduction_count"] = 0
        employee_dict["new_business_sum"] = 0
        employee_dict["exchange_count"] = 0
        employee_dict["inst_to_exchange"] = 0

        if hub:
            for hub_instance in instance.hub.all():
                if hub == hub_instance.slug:
                    overview_list.append(employee_dict)
        else:
            overview_list.append(employee_dict)

    for instance in overview_list:
        for instruction_instance in sales_instructions:
            if instance["id"] == instruction_instance["employee_id"]:
                instance["instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
                instance["total_instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
                instance["instruction_fee_avg"] = instruction_instance[
                    "instruction_fee_avg"
                ]
                instance["instruction_list_price_avg"] = instruction_instance[
                    "instruction_list_price_avg"
                ]

        for instruction_instance in lettings_instructions:
            if instance["id"] == instruction_instance["employee_id"]:
                instance["lettings_instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
                instance["total_instruction_count"] += instruction_instance[
                    "instruction_count"
                ]
                instance[
                    "lettings_instruction_fee_avg"
                ] = instruction_instance["instruction_fee_avg"]
                instance[
                    "lettings_instruction_list_price_avg"
                ] = instruction_instance["instruction_list_price_avg"]

        for valuation_instance in valuations:
            if instance["id"] == valuation_instance["employee_id"]:
                instance["valuation_count"] = valuation_instance[
                    "valuation_count"
                ]

        for all_inst_instance in instruction_reductions:
            if instance["id"] == all_inst_instance.propertyprocess.employee.id:
                if all_inst_instance.reduced > 0:
                    instance["reduction_val"] += 1

        for exchange_inst in exchanges_sales:
            if (
                instance["id"]
                == exchange_inst.exchange.propertyprocess.employee.id
            ):
                instance["exchange_count"] += 1

        for exchange_inst in exchanges_lettings:
            if (
                instance["id"]
                == exchange_inst.exchange.propertyprocess.employee.id
            ):
                instance["exchange_count"] += 1

        try:
            instance["val_to_inst"] = round(
                instance["total_instruction_count"]
                / instance["valuation_count"]
                * 100,
                2,
            )
        except ZeroDivisionError:
            instance["val_to_inst"] = 0

        try:
            instance["reduction_val"] = round(
                instance["reduction_val"]
                / instance["total_instruction_count"]
                * 100,
                2,
            )
        except ZeroDivisionError:
            instance["reduction_val"] = 0

        try:
            instance["inst_to_exchange"] = round(
                instance["exchange_count"]
                / instance["total_instruction_count"]
                * 100,
                2,
            )
        except ZeroDivisionError:
            instance["inst_to_exchange"] = 0

        if (
            instance["valuation_count"] == 0
            and instance["instruction_count"] == 0
            and instance["lettings_instruction_count"] == 0
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
        "hub": hub,
        "sort": sort,
        "direction": direction,
        "stats": stats,
    }

    return render(request, "stats/extra_stats.html", context)


@otp_required
@login_required
def hub_extra_stats(request):
    """
    A view to return hub extra stats & total company
    """

    filter = "current_quarter"
    link_to_hub = "propertyprocess__hub"
    ex_link_to_hub = "exchange__propertyprocess__hub"
    hub = "propertyprocess__hub__id"
    ex_hub = "exchange__propertyprocess__hub__id"
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

    all_valuations = Valuation.objects.exclude(active=False).filter(
        date__range=[start_date, end_date],
    )

    valuations = (
        all_valuations.values(hub)
        .annotate(valuation_count=Count(link_to_hub))
        .order_by("-valuation_count")
    )

    all_instructions = Instruction.objects.exclude(active=False).filter(
        date__range=[start_date, end_date],
    )

    instruction_reductions = all_instructions.annotate(
        reduced=Count("propertyprocess__reduction")
    )

    instructions = (
        all_instructions.values(hub)
        .annotate(instruction_count=Count(link_to_hub))
        .order_by("-instruction_count")
    )

    sales_inst = all_instructions.filter(
        propertyprocess__sector=PropertyProcess.SALES,
    )

    lettings_inst = all_instructions.filter(
        propertyprocess__sector=PropertyProcess.LETTINGS,
    )

    sales_instructions = (
        sales_inst.values(hub)
        .annotate(instruction_fee_avg=Avg("fee_agreed"))
        .annotate(instruction_count=Count(link_to_hub))
        .annotate(instruction_list_price_avg=Avg("listing_price"))
        .order_by("-instruction_fee_avg")
    )

    lettings_instructions = (
        lettings_inst.values(hub)
        .annotate(instruction_fee_avg=Avg("fee_agreed"))
        .annotate(instruction_count=Count(link_to_hub))
        .annotate(instruction_list_price_avg=Avg("listing_price"))
        .order_by("-instruction_fee_avg")
    )

    exchanges_sales = ExchangeMoveSales.objects.filter(
        exchange_date__range=[start_date, end_date],
    ).order_by("-exchange_date")

    exchanges_lettings = ExchangeMoveLettings.objects.filter(
        move_in_date__range=[start_date, end_date],
    ).order_by("-move_in_date")

    for instance in instructions:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in sales_instructions:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in lettings_instructions:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in valuations:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    hubs = Hub.objects.filter(is_active=True)

    sales_inst_fee = sales_inst.aggregate(
        instruction_fee_avg=Avg("fee_agreed")
    )
    sales_inst_price = sales_inst.aggregate(
        instruction_list_price_avg=Avg("listing_price")
    )
    lettings_inst_fee = lettings_inst.aggregate(
        instruction_fee_avg=Avg("fee_agreed")
    )
    lettings_inst_price = lettings_inst.aggregate(
        instruction_list_price_avg=Avg("listing_price")
    )

    reduction_val = 0
    exchange_count = len(exchanges_sales) + len(exchanges_lettings)

    sales_days = exchanges_sales.aggregate(
        avg_days=Avg(
            F("exchange_date") - F("exchange__propertyprocess__deal__date")
        )
    )
    days_and_time = sales_days["avg_days"]
    if days_and_time is None:
        sales_weeks = 0
    else:
        sales_weeks = days_and_time.days / 7

    hub_sales_days = (
        exchanges_sales.values(ex_hub)
        .annotate(exchange_count=Count(ex_link_to_hub))
        .annotate(
            avg_days=Avg(
                F("exchange_date") - F("exchange__propertyprocess__deal__date")
            )
        )
        .order_by("-exchange_count")
    )

    hub_lettings_days = (
        exchanges_lettings.values(ex_hub)
        .annotate(exchange_count=Count(ex_link_to_hub))
        .annotate(
            avg_days=Avg(
                F("move_in_date") - F("exchange__propertyprocess__deal__date")
            )
        )
        .order_by("-exchange_count")
    )

    lettings_days = exchanges_lettings.aggregate(
        avg_days=Avg(
            F("move_in_date") - F("exchange__propertyprocess__deal__date")
        )
    )
    lettings_days_and_time = lettings_days["avg_days"]
    if lettings_days_and_time is None:
        lettings_weeks = 0
    else:
        lettings_weeks = lettings_days_and_time.days / 7

    for instance in instruction_reductions:
        if instance.reduced > 0:
            reduction_val += 1

    try:
        val_to_inst = round(
            len(all_instructions) / len(all_valuations) * 100,
            2,
        )
    except ZeroDivisionError:
        val_to_inst = 0

    try:
        reduction_val = round(
            reduction_val / len(all_instructions) * 100,
            2,
        )
    except ZeroDivisionError:
        reduction_val = 0

    try:
        inst_to_exchange = round(
            exchange_count / len(all_instructions) * 100,
            2,
        )
    except ZeroDivisionError:
        inst_to_exchange = 0

    overview_list = []
    stats = []
    total = {
        "sales_instruction_count": len(sales_inst),
        "lettings_instruction_count": len(lettings_inst),
        "instruction_fee_avg": sales_inst_fee["instruction_fee_avg"],
        "lettings_instruction_fee_avg": lettings_inst_fee[
            "instruction_fee_avg"
        ],
        "instruction_price_avg": sales_inst_price[
            "instruction_list_price_avg"
        ],
        "lettings_instruction_price_avg": lettings_inst_price[
            "instruction_list_price_avg"
        ],
        "val_to_inst": val_to_inst,
        "reduction_val": reduction_val,
        "inst_to_exchange": inst_to_exchange,
        "sales_weeks": sales_weeks,
        "lettings_weeks": lettings_weeks,
    }

    for instance in hubs:
        hub_dict = {}
        hub_dict["id"] = instance.id
        hub_dict["hub_name"] = instance.hub_name

        hub_dict["valuation_count"] = 0
        hub_dict["val_to_inst"] = 0
        hub_dict["reduction_val"] = 0
        hub_dict["instruction_count"] = 0
        hub_dict["total_instruction_count"] = 0
        hub_dict["instruction_fee_avg"] = 0
        hub_dict["instruction_list_price_avg"] = 0
        hub_dict["lettings_instruction_count"] = 0
        hub_dict["lettings_instruction_fee_avg"] = 0
        hub_dict["lettings_instruction_list_price_avg"] = 0
        hub_dict["reduction_count"] = 0
        hub_dict["new_business_sum"] = 0
        hub_dict["exchange_count"] = 0
        hub_dict["inst_to_exchange"] = 0
        hub_dict["sales_weeks"] = 0
        hub_dict["lettings_weeks"] = 0

        overview_list.append(hub_dict)

    for instance in overview_list:
        for instruction_instance in sales_instructions:
            if instance["id"] == instruction_instance["hub_id"]:
                instance["instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
                instance["total_instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
                instance["instruction_fee_avg"] = instruction_instance[
                    "instruction_fee_avg"
                ]
                instance["instruction_list_price_avg"] = instruction_instance[
                    "instruction_list_price_avg"
                ]

        for instruction_instance in lettings_instructions:
            if instance["id"] == instruction_instance["hub_id"]:
                instance["lettings_instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
                instance["total_instruction_count"] += instruction_instance[
                    "instruction_count"
                ]
                instance[
                    "lettings_instruction_fee_avg"
                ] = instruction_instance["instruction_fee_avg"]
                instance[
                    "lettings_instruction_list_price_avg"
                ] = instruction_instance["instruction_list_price_avg"]

        for valuation_instance in valuations:
            if instance["id"] == valuation_instance["hub_id"]:
                instance["valuation_count"] = valuation_instance[
                    "valuation_count"
                ]

        for all_inst_instance in instruction_reductions:
            if instance["id"] == all_inst_instance.propertyprocess.hub.id:
                if all_inst_instance.reduced > 0:
                    instance["reduction_val"] += 1

        for exchange_inst in exchanges_sales:
            if instance["id"] == exchange_inst.exchange.propertyprocess.hub.id:
                instance["exchange_count"] += 1

        for exchange_inst in exchanges_lettings:
            if instance["id"] == exchange_inst.exchange.propertyprocess.hub.id:
                instance["exchange_count"] += 1

        for hub_exchange_inst in hub_sales_days:
            if (
                instance["id"]
                == hub_exchange_inst["exchange__propertyprocess__hub__id"]
            ):
                instance["sales_weeks"] = (
                    hub_exchange_inst["avg_days"].days / 7
                )

        for hub_exchange_inst in hub_lettings_days:
            if (
                instance["id"]
                == hub_exchange_inst["exchange__propertyprocess__hub__id"]
            ):
                instance["lettings_weeks"] = (
                    hub_exchange_inst["avg_days"].days / 7
                )

        try:
            instance["val_to_inst"] = round(
                instance["total_instruction_count"]
                / instance["valuation_count"]
                * 100,
                2,
            )
        except ZeroDivisionError:
            instance["val_to_inst"] = 0

        try:
            instance["reduction_val"] = round(
                instance["reduction_val"]
                / instance["total_instruction_count"]
                * 100,
                2,
            )
        except ZeroDivisionError:
            instance["reduction_val"] = 0

        try:
            instance["inst_to_exchange"] = round(
                instance["exchange_count"]
                / instance["total_instruction_count"]
                * 100,
                2,
            )
        except ZeroDivisionError:
            instance["inst_to_exchange"] = 0

        if (
            instance["valuation_count"] == 0
            and instance["instruction_count"] == 0
            and instance["lettings_instruction_count"] == 0
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
        "hub": hub,
        "sort": sort,
        "direction": direction,
        "stats": stats,
        "total": total,
    }

    return render(request, "stats/hub_extra_stats.html", context)


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


@otp_required
@login_required
def hub_filters(request):
    """
    A view to return an ajax response with hub filters
    """

    data = dict()

    hub = None

    if "hub" in request.GET:
        hub = request.GET.get("hub")

    hubs = Hub.objects.filter(is_active=True).order_by("hub_name")

    context = {
        "hub": hub,
        "hubs": hubs,
    }

    data["html_modal"] = render_to_string(
        "stats/includes/hub_form_modal.html", request=request, context=context
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
        exchange_dict[
            "property_proccess"
        ] = instance.exchange.propertyprocess.id
        exchange_dict["date"] = instance.exchange_date
        exchange_dict["comp_date"] = instance.completion_date

        property_fees = instance.exchange.propertyprocess.property_fees.all()
        filtered_property_fees = property_fees.filter(active=True)

        sum = 0
        for filtered_property_fee in filtered_property_fees:
            sum += filtered_property_fee.new_business

        exchange_dict["sum"] = sum
        exchange_dict[
            "fee"
        ] = instance.exchange.propertyprocess.property_fees_master.fee
        exchange_dict[
            "final_price"
        ] = instance.exchange.propertyprocess.property_fees_master.price

        exchanges.append(exchange_dict)

    for instance in exchanges_lettings:
        exchange_dict = {}
        exchange_dict["id"] = instance.id
        exchange_dict["address"] = instance.exchange.propertyprocess
        exchange_dict["sector"] = instance.exchange.propertyprocess.sector
        exchange_dict[
            "property_proccess"
        ] = instance.exchange.propertyprocess.id
        exchange_dict["date"] = instance.move_in_date

        property_fees = instance.exchange.propertyprocess.property_fees.all()
        filtered_property_fees = property_fees.filter(active=True)

        sum = 0
        for filtered_property_fee in filtered_property_fees:
            sum += filtered_property_fee.new_business

        exchange_dict["sum"] = sum

        exchange_dict[
            "fee"
        ] = instance.exchange.propertyprocess.property_fees_master.fee
        exchange_dict[
            "final_price"
        ] = instance.exchange.propertyprocess.property_fees_master.price

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

    new_business = PropertyFees.objects.filter(
        propertyprocess__employee__id=profile_id,
        date__range=[start_date, end_date],
        active=True,
        show_all=True,
    ).order_by("-date")

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

    reductions = Reduction.objects.filter(
        propertyprocess__employee__id=profile_id,
        date__range=[start_date, end_date],
    ).order_by("-date")

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


@otp_required
@login_required
def export_overview_xls(request):
    """
    Export to excel the stats overview
    """

    filter = "current_quarter"
    link_to_employee = "propertyprocess__employee"
    employee = "propertyprocess__employee__id"
    hub = None
    sort = None
    direction = None

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if "hub" in request.GET:
        hub = request.GET.get("hub")

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
        employee_dict["hub"] = instance.hub.first().hub_name
        employee_dict["valuation_count"] = 0
        employee_dict["instruction_count"] = 0
        employee_dict["reduction_count"] = 0
        employee_dict["new_business_sum"] = 0
        employee_dict["exchange_sum"] = 0

        if hub:
            for hub_instance in instance.hub.all():
                if hub == hub_instance.slug:
                    overview_list.append(employee_dict)
        else:
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
            if (
                instance["id"]
                == exchanges_sales_instance.exchange.propertyprocess.employee.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_sales_instance.exchange.propertyprocess.property_fees_master.new_business
                )

        for exchanges_lettings_instance in exchanges_lettings:
            if (
                instance["id"]
                == exchanges_lettings_instance.exchange.propertyprocess.employee.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_lettings_instance.exchange.propertyprocess.property_fees_master.new_business
                )

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

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="Stats Overview {start_date} to {end_date}.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Overview")

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = [
        "Date Range",
        start_date,
        end_date,
    ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Name",
        "Hub",
        "Active",
        "Valuations",
        "Instructions",
        "Reductions",
        "New Business",
        "Exchanges",
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = "0.00"

    for instance in stats:
        row_num += 1
        col_num = 0

        ws.write(row_num, col_num, instance["name"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["hub"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["active"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["valuation_count"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["instruction_count"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["reduction_count"], font_style)
        col_num += 1

        ws.write(
            row_num, col_num, instance["new_business_sum"], money_font_style
        )
        col_num += 1

        ws.write(row_num, col_num, instance["exchange_sum"], money_font_style)
        col_num += 1

    wb.save(response)
    return response


@otp_required
@login_required
def export_hub_overview_xls(request):
    """
    Export to excel the stats overview for hubs
    """

    filter = "current_quarter"
    link_to_hub = "propertyprocess__hub"
    hub = "propertyprocess__hub__id"
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
        Valuation.objects.values(hub)
        .exclude(active=False)
        .annotate(valuation_count=Count(link_to_hub))
        .filter(
            date__range=[start_date, end_date],
        )
        .order_by("-valuation_count")
    )

    instructions = (
        Instruction.objects.values(hub)
        .exclude(active=False)
        .annotate(instruction_count=Count(link_to_hub))
        .filter(
            date__range=[start_date, end_date],
        )
        .order_by("-instruction_count")
    )

    reductions = (
        Reduction.objects.values(hub)
        .annotate(reduction_count=Count(link_to_hub))
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
        PropertyFees.objects.values(hub)
        .annotate(new_business_sum=Sum("new_business"))
        .filter(
            date__range=[start_date, end_date],
            active=True,
            show_all=True,
        )
        .order_by("-new_business_sum")
    )

    for instance in valuations:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in instructions:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in reductions:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    for instance in new_business:
        instance["hub_id"] = instance["propertyprocess__hub__id"]
        del instance["propertyprocess__hub__id"]

    hubs = Hub.objects.filter(is_active=True)

    overview_list = []
    stats = []

    for instance in hubs:
        hub_dict = {}
        hub_dict["id"] = instance.id
        hub_dict["hub_name"] = instance.hub_name

        hub_dict["valuation_count"] = 0
        hub_dict["instruction_count"] = 0
        hub_dict["reduction_count"] = 0
        hub_dict["new_business_sum"] = 0
        hub_dict["exchange_sum"] = 0

        overview_list.append(hub_dict)

    for instance in overview_list:
        for valuation_instance in valuations:
            if instance["id"] == valuation_instance["hub_id"]:
                instance["valuation_count"] = valuation_instance[
                    "valuation_count"
                ]
        for instruction_instance in instructions:
            if instance["id"] == instruction_instance["hub_id"]:
                instance["instruction_count"] = instruction_instance[
                    "instruction_count"
                ]
        for reduction_instance in reductions:
            if instance["id"] == reduction_instance["hub_id"]:
                instance["reduction_count"] = reduction_instance[
                    "reduction_count"
                ]
        for new_business_instance in new_business:
            if instance["id"] == new_business_instance["hub_id"]:
                instance["new_business_sum"] = new_business_instance[
                    "new_business_sum"
                ]

        for exchanges_sales_instance in exchanges_sales:
            if (
                instance["id"]
                == exchanges_sales_instance.exchange.propertyprocess.hub.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_sales_instance.exchange.propertyprocess.property_fees_master.new_business
                )

        for exchanges_lettings_instance in exchanges_lettings:
            if (
                instance["id"]
                == exchanges_lettings_instance.exchange.propertyprocess.hub.id
            ):
                instance[
                    "exchange_sum"
                ] += (
                    exchanges_lettings_instance.exchange.propertyprocess.property_fees_master.new_business
                )

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

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="Hub Stats Overview {start_date} to {end_date}.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Overview")

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = [
        "Date Range",
        start_date,
        end_date,
    ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Hub",
        "Valuations",
        "Instructions",
        "Reductions",
        "New Business",
        "Exchanges",
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = "0.00"

    for instance in stats:
        row_num += 1
        col_num = 0

        ws.write(row_num, col_num, instance["hub_name"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["valuation_count"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["instruction_count"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["reduction_count"], font_style)
        col_num += 1

        ws.write(
            row_num, col_num, instance["new_business_sum"], money_font_style
        )
        col_num += 1

        ws.write(row_num, col_num, instance["exchange_sum"], money_font_style)
        col_num += 1

    wb.save(response)
    return response


@otp_required
@login_required
def export_hub_valuations_xls(request, hub_id):
    """
    Export to excel the valuations for a hub
    """

    filter = "current_quarter"

    selected_hub = Hub.objects.get(id=hub_id)

    if "filter" in request.GET:
        filter = request.GET.get("filter")

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
        Valuation.objects.exclude(active=False)
        .filter(
            propertyprocess__hub=selected_hub.id,
            date__range=[start_date, end_date],
        )
        .order_by("-date")
    )

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{selected_hub.hub_name} Valuations {start_date} to {end_date}.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Valuations")

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = [
        "Date Range",
        start_date,
        end_date,
    ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Address",
        "Type",
        "Valuer",
        "Valuation Date",
        "Fee Quoted (%)",
        "Price Quoted (£)",
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = "0.00"

    val_list = []

    for instance in valuations:
        val_instance = {}
        val_instance["address"] = instance.propertyprocess.property.address
        val_instance["sector"] = instance.propertyprocess.sector
        val_instance["name"] = instance.valuer.user.get_full_name()
        val_instance["date"] = instance.date.strftime("%d-%m-%Y")
        val_instance["fee"] = instance.fee_quoted
        val_instance["price"] = instance.price_quoted
        val_list.append(val_instance)

    for instance in val_list:
        row_num += 1
        col_num = 0

        ws.write(row_num, col_num, instance["address"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["sector"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["name"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["date"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["fee"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["price"], money_font_style)
        col_num += 1

    wb.save(response)

    return response


@otp_required
@login_required
def export_hub_instructions_xls(request, hub_id):
    """
    Export to excel the instructions for a hub
    """

    filter = "current_quarter"

    selected_hub = Hub.objects.get(id=hub_id)

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if filter == "current_quarter":
        date_calc_data = date_calc(timezone.now(), filter)
        start_date = date_calc_data["start_date"]
        end_date = date_calc_data["end_date"]
    else:
        start_date = request.GET.get("start-date")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        end_date = request.GET.get("end-date")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    instructions = (
        Instruction.objects.exclude(active=False)
        .filter(
            propertyprocess__hub=selected_hub.id,
            date__range=[start_date, end_date],
        )
        .order_by("-date")
    )

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{selected_hub.hub_name} Instructions {start_date} to {end_date}.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Instructions")

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = [
        "Date Range",
        start_date,
        end_date,
    ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Address",
        "Type",
        "Employee",
        "Instructed Date",
        "Fee At Instruction (%)",
        "Listing Price (£)",
        "Agreement Type",
        "Length of Contract",
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = "0.00"

    inst_list = []

    for instance in instructions:
        inst_instance = {}
        inst_instance["address"] = instance.propertyprocess.property.address
        inst_instance["sector"] = instance.propertyprocess.sector
        inst_instance[
            "name"
        ] = instance.propertyprocess.employee.user.get_full_name()
        inst_instance["date"] = instance.date.strftime("%d-%m-%Y")
        inst_instance["fee"] = instance.fee_agreed
        inst_instance["price"] = instance.listing_price
        inst_instance["agreement_type"] = instance.agreement_type
        inst_instance["length_of_contract"] = instance.length_of_contract
        inst_list.append(inst_instance)

    for instance in inst_list:
        row_num += 1
        col_num = 0

        ws.write(row_num, col_num, instance["address"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["sector"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["name"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["date"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["fee"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["price"], money_font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["agreement_type"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["length_of_contract"], font_style)
        col_num += 1

    wb.save(response)

    return response


@otp_required
@login_required
def export_hub_reductions_xls(request, hub_id):
    """
    Export to excel the reductions for a hub
    """

    filter = "current_quarter"

    selected_hub = Hub.objects.get(id=hub_id)

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if filter == "current_quarter":
        date_calc_data = date_calc(timezone.now(), filter)
        start_date = date_calc_data["start_date"]
        end_date = date_calc_data["end_date"]
    else:
        start_date = request.GET.get("start-date")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        end_date = request.GET.get("end-date")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    reductions = Reduction.objects.filter(
        propertyprocess__hub=selected_hub.id,
        date__range=[start_date, end_date],
    ).order_by("-date")

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{selected_hub.hub_name} Reductions {start_date} to {end_date}.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Reductions")

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = [
        "Date Range",
        start_date,
        end_date,
    ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Address",
        "Type",
        "Employee",
        "Reduction Date",
        "New Price (£)",
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = "0.00"

    red_list = []

    for instance in reductions:
        red_instance = {}
        red_instance["address"] = instance.propertyprocess.property.address
        red_instance["sector"] = instance.propertyprocess.sector
        red_instance[
            "name"
        ] = instance.propertyprocess.employee.user.get_full_name()
        red_instance["date"] = instance.date.strftime("%d-%m-%Y")
        red_instance["price"] = instance.price_change
        red_list.append(red_instance)

    for instance in red_list:
        row_num += 1
        col_num = 0

        ws.write(row_num, col_num, instance["address"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["sector"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["name"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["date"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["price"], money_font_style)
        col_num += 1

    wb.save(response)

    return response


@otp_required
@login_required
def export_hub_new_business_xls(request, hub_id):
    """
    Export to excel the new business for a hub
    """

    filter = "current_quarter"

    selected_hub = Hub.objects.get(id=hub_id)

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if filter == "current_quarter":
        date_calc_data = date_calc(timezone.now(), filter)
        start_date = date_calc_data["start_date"]
        end_date = date_calc_data["end_date"]
    else:
        start_date = request.GET.get("start-date")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        end_date = request.GET.get("end-date")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    new_business = (
        PropertyFees.objects.exclude(active=False)
        .exclude(show_all=False)
        .filter(
            propertyprocess__hub=selected_hub.id,
            date__range=[start_date, end_date],
        )
        .order_by("-date")
    )

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{selected_hub.hub_name} New Business {start_date} to {end_date}.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("New Business")

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = [
        "Date Range",
        start_date,
        end_date,
    ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Address",
        "Type",
        "Employee",
        "Deal Date",
        "Fee (%)",
        "Price (£)",
        "New Business Amount (£)",
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = "0.00"

    new_business_list = []

    for instance in new_business:
        new_business_instance = {}
        new_business_instance[
            "address"
        ] = instance.propertyprocess.property.address
        new_business_instance["sector"] = instance.propertyprocess.sector
        new_business_instance[
            "name"
        ] = instance.propertyprocess.employee.user.get_full_name()
        new_business_instance["date"] = instance.date.strftime("%d-%m-%Y")
        new_business_instance["fee"] = instance.fee
        new_business_instance["price"] = instance.price
        new_business_instance["new_business"] = instance.new_business
        new_business_list.append(new_business_instance)

    for instance in new_business_list:
        row_num += 1
        col_num = 0

        ws.write(row_num, col_num, instance["address"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["sector"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["name"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["date"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["fee"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["price"], money_font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["new_business"], money_font_style)
        col_num += 1

    wb.save(response)

    return response


@otp_required
@login_required
def export_hub_exchanges_xls(request, hub_id):
    """
    Export to excel the exchanges for a hub
    """

    filter = "current_quarter"

    selected_hub = Hub.objects.get(id=hub_id)

    if "filter" in request.GET:
        filter = request.GET.get("filter")

    if filter == "current_quarter":
        date_calc_data = date_calc(timezone.now(), filter)
        start_date = date_calc_data["start_date"]
        end_date = date_calc_data["end_date"]
    else:
        start_date = request.GET.get("start-date")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        end_date = request.GET.get("end-date")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    exchanges_sales = ExchangeMoveSales.objects.filter(
        exchange__propertyprocess__hub=selected_hub.id,
        exchange_date__range=[start_date, end_date],
    ).order_by("-exchange_date")

    exchanges_lettings = ExchangeMoveLettings.objects.filter(
        exchange__propertyprocess__hub=selected_hub.id,
        move_in_date__range=[start_date, end_date],
    ).order_by("-move_in_date")

    exchanges = []

    for instance in exchanges_sales:
        exchange_instance = {}
        exchange_instance[
            "address"
        ] = instance.exchange.propertyprocess.property.address
        exchange_instance["sector"] = instance.exchange.propertyprocess.sector
        exchange_instance[
            "name"
        ] = instance.exchange.propertyprocess.employee.user.get_full_name()

        property_fees = instance.exchange.propertyprocess.property_fees.all()
        filtered_property_fees = property_fees.filter(active=True)

        sum = 0
        for filtered_property_fee in filtered_property_fees:
            sum += filtered_property_fee.new_business

        exchange_instance["new_business"] = sum
        exchange_instance[
            "fee"
        ] = instance.exchange.propertyprocess.property_fees_master.fee
        exchange_instance["date"] = instance.exchange_date.strftime("%d-%m-%Y")
        exchange_instance["comp_date"] = instance.completion_date.strftime(
            "%d-%m-%Y"
        )
        exchange_instance[
            "price"
        ] = instance.exchange.propertyprocess.property_fees_master.price
        exchanges.append(exchange_instance)

    for instance in exchanges_lettings:
        exchange_instance = {}
        exchange_instance[
            "address"
        ] = instance.exchange.propertyprocess.property.address
        exchange_instance["sector"] = instance.exchange.propertyprocess.sector
        exchange_instance[
            "name"
        ] = instance.exchange.propertyprocess.employee.user.get_full_name()

        property_fees = instance.exchange.propertyprocess.property_fees.all()
        filtered_property_fees = property_fees.filter(active=True)

        sum = 0
        for filtered_property_fee in filtered_property_fees:
            sum += filtered_property_fee.new_business

        exchange_instance["new_business"] = sum
        exchange_instance[
            "fee"
        ] = instance.exchange.propertyprocess.property_fees_master.fee
        exchange_instance["date"] = instance.move_in_date.strftime("%d-%m-%Y")
        exchange_instance["comp_date"] = ""
        exchange_instance[
            "price"
        ] = instance.exchange.propertyprocess.property_fees_master.price
        exchanges.append(exchange_instance)

    exchanges = sorted(
        exchanges,
        key=lambda k: k["date"],
        reverse=True,
    )

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type="application/ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{selected_hub.hub_name} Exchanges {start_date} to {end_date}.xls"'

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Exchanges")

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = [
        "Date Range",
        start_date,
        end_date,
    ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Address",
        "Type",
        "Employee",
        "Fee (£)",
        "Fee (%)",
        "Exchange/Move In Date",
        "Completion Date",
        "Final Price (£)",
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = "0.00"

    for instance in exchanges:
        row_num += 1
        col_num = 0

        ws.write(row_num, col_num, instance["address"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["sector"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["name"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["new_business"], money_font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["fee"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["date"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["comp_date"], font_style)
        col_num += 1

        ws.write(row_num, col_num, instance["price"], money_font_style)
        col_num += 1

    wb.save(response)

    return response


@otp_required
@login_required
def pipeline(request):

    hubs = Hub.objects.filter(is_active=True).exclude(slug="all-hubs").exclude(slug="weekend-directors")

    deal_properties = PropertyFees.objects.filter(
        propertyprocess__macro_status=4, active=True, show_all=True
    )

    total_pipeline = deal_properties.aggregate(
        total_pipeline=Sum("new_business")
    )

    pipeline = []

    dict = {}
    dict["id"] = 0
    dict["name"] = "Total Pipeline"
    dict["pipeline"] = total_pipeline["total_pipeline"]

    pipeline.append(dict)

    for instance in hubs:
        hub_deal_properties = deal_properties.filter(
            propertyprocess__hub=instance.id
        )
        hub_pipeline = hub_deal_properties.aggregate(
            total_pipeline=Sum("new_business")
        )

        dict = {}
        dict["id"] = instance.id
        dict["name"] = instance.hub_name
        dict["pipeline"] = hub_pipeline["total_pipeline"]

        pipeline.append(dict)

    template = "stats/pipeline.html"

    context = {
        "pipeline": pipeline,
    }

    return render(request, template, context)


@director_required
@staff_member_required
@otp_required
@login_required
def individual_reporting_page(request):

    data = dict()

    users = Profile.objects.filter(user__is_active=True) \
    .filter(employee_targets=True) \
    .order_by("user__first_name")

    selected_user = None
    if "user" in request.GET:
        user_uuid = request.GET.get("user")
        selected_user = Profile.objects.get(id=user_uuid)

    quarters = calculate_quarter_and_year(timezone.now())

    user_data = []

    if selected_user is not None:
        for idx, quarter in enumerate(quarters):

            quarter_info = {}

            for key, value in quarter.items():
                if key == "start_year":
                    year = value
                elif key == "start_month":
                    start_month = value
                elif key == "end_month":
                    end_month = value
                elif key == "company_year":
                    company_year = str(value)
                elif key == "quarter":
                    current_quarter = value
                    quarter_info["quarter"] = value

            valuation_count = (
                Valuation.objects.filter(valuer=selected_user.id)
                .exclude(active=False)
                .filter(
                    date__iso_year=year,
                    date__month__gte=start_month,
                    date__month__lte=end_month,
                    propertyprocess__employee__employee_targets=True,
                    propertyprocess__employee__user__is_active=True,
                ).count()
            )

            instruction_count = (
                Instruction.objects.filter(propertyprocess__employee=selected_user.id)
                .exclude(active=False)
                .filter(
                    date__iso_year=year,
                    date__month__gte=start_month,
                    date__month__lte=end_month,
                    propertyprocess__employee__employee_targets=True,
                    propertyprocess__employee__user__is_active=True,
                ).count()
            )

            reduction_count = (
                Reduction.objects.filter(propertyprocess__employee=selected_user.id)
                .filter(
                    date__iso_year=year,
                    date__month__gte=start_month,
                    date__month__lte=end_month,
                    propertyprocess__employee__employee_targets=True,
                    propertyprocess__employee__user__is_active=True,
                ).count()
            )

            new_business = (
                PropertyFees.objects.values("propertyprocess__employee__id")
                .filter(propertyprocess__employee__id=selected_user.id)
                .annotate(new_business_sum=Sum("new_business"))
                .filter(
                    date__iso_year=year,
                    date__month__gte=start_month,
                    date__month__lte=end_month,
                    propertyprocess__employee__employee_targets=True,
                    propertyprocess__employee__user__is_active=True,
                    active=True,
                    show_all=True,
                )
                .order_by("-new_business_sum")
            )

            exchanges_sales = (
                ExchangeMoveSales.objects.filter(exchange__propertyprocess__employee__id=selected_user.id)
                .filter(
                    exchange_date__iso_year=year,
                    exchange_date__month__gte=start_month,
                    exchange_date__month__lte=end_month,
                    exchange__propertyprocess__employee__employee_targets=True,
                    exchange__propertyprocess__employee__user__is_active=True
                )
                .order_by("-exchange_date")
            )

            exchanges_lettings = (
                ExchangeMoveLettings.objects.filter(exchange__propertyprocess__employee__id=selected_user.id)
                .filter(
                    move_in_date__iso_year=year,
                    move_in_date__month__gte=start_month,
                    move_in_date__month__lte=end_month,
                    exchange__propertyprocess__employee__employee_targets=True,
                    exchange__propertyprocess__employee__user__is_active=True
                )
                .order_by("-move_in_date")
            )

            exchange_sum = 0

            for exchanges_sales_instance in exchanges_sales:
                exchange_sum += (
                    exchanges_sales_instance.exchange.propertyprocess.property_fees_master.new_business
                )

            for exchanges_lettings_instance in exchanges_lettings:
                exchange_sum += (
                    exchanges_lettings_instance.exchange.propertyprocess.property_fees_master.new_business
                )
            
            try:
                targets = UserTargets.objects.get(
                    profile_targets=selected_user.id,
                    year=company_year,
                    quarter=current_quarter
                )
            except:
                targets = None
            
            if targets is None:
                quarter_info["valuation_target"] = 0
                quarter_info["instruction_target"] = 0
                quarter_info["reduction_target"] = 0
                quarter_info["new_business_target"] = 0
                quarter_info["exchange_sum_target"] = 0
            else:
                quarter_info["valuation_target"] = targets.valuations
                quarter_info["instruction_target"] = targets.instructions
                quarter_info["reduction_target"] = targets.reductions
                quarter_info["new_business_target"] = targets.new_business
                quarter_info["exchange_sum_target"] = targets.exchange_and_move

            quarter_info["valuations"] = valuation_count
            quarter_info["instructions"] = instruction_count
            quarter_info["reductions"] = reduction_count

            for result in new_business:
                for key, value in result.items():
                    if key == "new_business_sum":
                        quarter_info["new_business"] = value
            
            quarter_info["exchange_sum"] = exchange_sum

            user_data.append(quarter_info)

    context = {
        "users": users,
        "selected_user": selected_user,
        "quarters": quarters,
        "user_data": user_data
    }

    return render(request, "stats/individual_reporting.html", context)
