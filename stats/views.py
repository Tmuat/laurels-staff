import datetime
import xlwt

from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse, HttpResponse
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
from regionandhub.models import Hub
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

    all_valuations = (
        Valuation.objects
        .exclude(active=False)
        .filter(
            date__range=[start_date, end_date],
        )
    )

    valuations = (
        all_valuations.values(hub)
        .annotate(valuation_count=Count(link_to_hub))
        .order_by("-valuation_count")
    )

    all_instructions = (
        Instruction.objects
        .exclude(active=False)
        .filter(
            date__range=[start_date, end_date],
        )
    )

    instructions = (
        all_instructions.values(hub)
        .annotate(instruction_count=Count(link_to_hub))
        .order_by("-instruction_count")
    )

    all_reductions = (
        Reduction.objects
        .filter(
            date__range=[start_date, end_date],
        )
    )

    reductions = (
        all_reductions.values(hub)
        .annotate(reduction_count=Count(link_to_hub))
        .order_by("-reduction_count")
    )

    all_exchanges_sales = (
        ExchangeMoveSales.objects
        .filter(
            exchange_date__range=[start_date, end_date],
        )
    )

    exchanges_sales = all_exchanges_sales.order_by("-exchange_date")

    all_exchanges_lettings = (
        ExchangeMoveLettings.objects
        .filter(
            move_in_date__range=[start_date, end_date],
        )
    )

    exchanges_lettings = all_exchanges_lettings.order_by("-move_in_date")

    all_new_business = (
        PropertyFees.objects
        .exclude(active=False)
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
            if instance["id"] == exchanges_sales_instance.exchange.propertyprocess.hub.id:
                instance["exchange_sum"] += exchanges_sales_instance.exchange.propertyprocess.property_fees.last().new_business

        for exchanges_lettings_instance in exchanges_lettings:
            if instance["id"] == exchanges_lettings_instance.exchange.propertyprocess.hub.id:
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

    for instance in all_new_business:
        total["new_business_sum"] += instance.new_business

    for instance in exchanges_sales:
        total["exchange_sum"] += (
            instance. \
                exchange.propertyprocess.property_fees. \
                    last().new_business
        )

    for instance in exchanges_lettings:
        total["exchange_sum"] += (
            instance. \
                exchange.propertyprocess.property_fees. \
                    last().new_business
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

    hubs = Hub.objects.filter(
        is_active=True
    ).order_by("hub_name")

    context = {
        "hub": hub,
        "hubs": hubs,
    }

    data["html_modal"] = render_to_string(
        "stats/includes/hub_form_modal.html",
        request=request,
        context=context
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

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = (
        f'attachment; filename="Stats Overview {start_date} to {end_date}.xls"'
    )

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Overview')

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = ['Date Range', start_date, end_date, ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Hub', 'Active', 'Valuations', 'Instructions', 'Reductions', 'New Business', 'Exchanges']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = '0.00'

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

        ws.write(row_num, col_num, instance["new_business_sum"], money_font_style)
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
            if instance["id"] == exchanges_sales_instance.exchange.propertyprocess.hub.id:
                instance["exchange_sum"] += exchanges_sales_instance.exchange.propertyprocess.property_fees.last().new_business

        for exchanges_lettings_instance in exchanges_lettings:
            if instance["id"] == exchanges_lettings_instance.exchange.propertyprocess.hub.id:
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

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = (
        f'attachment; filename="Hub Stats Overview {start_date} to {end_date}.xls"'
    )

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Overview')

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = ['Date Range', start_date, end_date, ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Hub', 'Valuations', 'Instructions', 'Reductions', 'New Business', 'Exchanges']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = '0.00'

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

        ws.write(row_num, col_num, instance["new_business_sum"], money_font_style)
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
        Valuation.objects
        .exclude(active=False)
        .filter(
            propertyprocess__hub=selected_hub.id,
            date__range=[start_date, end_date],
        )
        .order_by("-date")
    )

    start_date = start_date.strftime("%d-%m-%Y")

    end_date = end_date.strftime("%d-%m-%Y")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = (
        f'attachment; filename="Hub Valuations {start_date} to {end_date}.xls"'
    )

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Valuations')

    # Add filters to first row of sheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    filter_columns = ['Date Range', start_date, end_date, ]

    for col_num in range(len(filter_columns)):
        ws.write(row_num, col_num, filter_columns[col_num], font_style)

    # Table header, starting row 3
    row_num += 2

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Address', 'Type', 'Valuer', 'Valuation Date', 'Fee Quoted (%)', 'Price Quoted (£)']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    money_font_style = xlwt.XFStyle()
    money_font_style.num_format_str = '0.00'

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
