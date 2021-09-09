from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from common.functions import (
    sales_progression_percentage,
    lettings_progression_percentage,
    quarter_and_year_calc,
    last_quarter_and_year_calc,
)
from home.forms import LettingsProgressorForm, ProgressorForm
from properties.models import (
    Offer,
    PropertyProcess,
    PropertyFees,
    Instruction,
    Reduction,
    Valuation,
    SalesProgression,
    LettingsProgression,
)
from regionandhub.models import Hub
from users.models import Profile, UserTargets


def top_performers(date):
    """
    Returns last quarters top performers.
    """

    data = dict()

    last_quarter_and_year = last_quarter_and_year_calc(date)

    year = last_quarter_and_year["start_year"]
    start_month = last_quarter_and_year["start_month"]
    end_month = last_quarter_and_year["end_month"]
    quarter = last_quarter_and_year["quarter"]
    company_year = last_quarter_and_year["company_year"]

    employee = "propertyprocess__employee__id"
    link_to_employee = "propertyprocess__employee"
    reductions = "propertyprocess__employee"

    valuations = (
        Valuation.objects.values("valuer")
        .exclude(active=False)
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

    instructions = (
        Instruction.objects.values(employee)
        .exclude(active=False)
        .annotate(instruction_count=Count(link_to_employee))
        .filter(
            date__iso_year=year,
            date__month__gte=start_month,
            date__month__lte=end_month,
            propertyprocess__employee__employee_targets=True,
            propertyprocess__employee__user__is_active=True,
        )
        .order_by("-instruction_count")
    )

    reductions = (
        Reduction.objects.values(employee)
        .annotate(reduction_count=Count(link_to_employee))
        .filter(
            date__iso_year=year,
            date__month__gte=start_month,
            date__month__lte=end_month,
            propertyprocess__employee__employee_targets=True,
            propertyprocess__employee__user__is_active=True,
        )
        .order_by("-reduction_count")
    )

    new_business = (
        PropertyFees.objects.values(employee)
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

    targets = UserTargets.objects.filter(year=company_year, quarter=quarter)

    # Renaming fields in querysets
    for instance in valuations:
        instance["employee_id"] = instance["valuer"]
        del instance["valuer"]

        instance["valuation_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    valuation_target = round(
                        instance["valuation_count"] / target.valuations * 100,
                        2,
                    )
                except ZeroDivisionError:
                    valuation_target = 0
                instance["valuation_target"] = valuation_target

    for instance in instructions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

        instance["instruction_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    instruction_target = round(
                        instance["instruction_count"]
                        / target.instructions
                        * 100,
                        2,
                    )
                except ZeroDivisionError:
                    instruction_target = 0
                instance["instruction_target"] = instruction_target

    for instance in reductions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

        instance["reduction_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    reduction_target = round(
                        instance["reduction_count"] / target.reductions * 100,
                        2,
                    )
                except ZeroDivisionError:
                    reduction_target = 0
                instance["reduction_target"] = reduction_target

    for instance in new_business:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

        instance["new_business_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    new_business_target = round(
                        instance["new_business_sum"]
                        / target.new_business
                        * 100,
                        2,
                    )
                except ZeroDivisionError:
                    new_business_target = 0
                instance["new_business_target"] = new_business_target

    valuations = sorted(
        valuations, key=lambda k: k["valuation_target"], reverse=True
    )

    instructions = sorted(
        instructions, key=lambda k: k["instruction_target"], reverse=True
    )

    reductions = sorted(
        reductions, key=lambda k: k["reduction_target"], reverse=True
    )

    new_business = sorted(
        new_business, key=lambda k: k["new_business_target"], reverse=True
    )

    data["valuations"] = valuations[:2]
    data["instructions"] = instructions[:2]
    data["reductions"] = reductions[:2]
    data["new_business"] = new_business[:2]

    return data


@otp_required
@login_required
def index(request):
    """A view to return the index page"""

    employees = Profile.objects.filter(
        employee_targets=True, user__is_active=True
    )

    quarter_and_year = quarter_and_year_calc(timezone.now())
    last_quarter_and_year = top_performers(timezone.now())

    last_valuations = last_quarter_and_year["valuations"]
    last_instructions = last_quarter_and_year["instructions"]
    last_reductions = last_quarter_and_year["reductions"]
    last_new_business = last_quarter_and_year["new_business"]

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]
    quarter = quarter_and_year["quarter"]
    company_year = quarter_and_year["company_year"]

    employee = "propertyprocess__employee__id"
    link_to_employee = "propertyprocess__employee"
    reductions = "propertyprocess__employee"

    valuations = (
        Valuation.objects.values("valuer")
        .exclude(active=False)
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

    instructions = (
        Instruction.objects.values(employee)
        .exclude(active=False)
        .annotate(instruction_count=Count(link_to_employee))
        .filter(
            date__iso_year=year,
            date__month__gte=start_month,
            date__month__lte=end_month,
            propertyprocess__employee__employee_targets=True,
            propertyprocess__employee__user__is_active=True,
        )
        .order_by("-instruction_count")
    )

    reductions = (
        Reduction.objects.values(employee)
        .annotate(reduction_count=Count(link_to_employee))
        .filter(
            date__iso_year=year,
            date__month__gte=start_month,
            date__month__lte=end_month,
            propertyprocess__employee__employee_targets=True,
            propertyprocess__employee__user__is_active=True,
        )
        .order_by("-reduction_count")
    )

    new_business = (
        PropertyFees.objects.values(employee)
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

    targets = UserTargets.objects.filter(year=company_year, quarter=quarter)

    # Renaming fields in querysets
    for instance in valuations:
        instance["employee_id"] = instance["valuer"]
        del instance["valuer"]

        instance["valuation_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    valuation_target = round(
                        instance["valuation_count"] / target.valuations * 100,
                        2,
                    )
                except ZeroDivisionError:
                    valuation_target = 0
                instance["valuation_target"] = valuation_target

    for instance in instructions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

        instance["instruction_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    instruction_target = round(
                        instance["instruction_count"]
                        / target.instructions
                        * 100,
                        2,
                    )
                except ZeroDivisionError:
                    instruction_target = 0
                instance["instruction_target"] = instruction_target

    for instance in reductions:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

        instance["reduction_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    reduction_target = round(
                        instance["reduction_count"] / target.reductions * 100,
                        2,
                    )
                except ZeroDivisionError:
                    reduction_target = 0
                instance["reduction_target"] = reduction_target

    for instance in new_business:
        instance["employee_id"] = instance["propertyprocess__employee__id"]
        del instance["propertyprocess__employee__id"]

        instance["new_business_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                try:
                    new_business_target = round(
                        instance["new_business_sum"]
                        / target.new_business
                        * 100,
                        2,
                    )
                except ZeroDivisionError:
                    new_business_target = 0
                instance["new_business_target"] = new_business_target

    valuations = sorted(
        valuations, key=lambda k: k["valuation_target"], reverse=True
    )

    instructions = sorted(
        instructions, key=lambda k: k["instruction_target"], reverse=True
    )

    reductions = sorted(
        reductions, key=lambda k: k["reduction_target"], reverse=True
    )

    new_business = sorted(
        new_business, key=lambda k: k["new_business_target"], reverse=True
    )

    # Creating lists of employees who haven't aren't on the lists
    no_valuation_employees = []
    no_instruction_employees = []
    no_reduction_employees = []
    no_new_business_employees = []

    for employee in employees:
        val_exist = False
        inst_exist = False
        red_exist = False
        new_exist = False
        for instance in valuations:
            if instance["employee_id"] == employee.id:
                val_exist = True
        for instance in instructions:
            if instance["employee_id"] == employee.id:
                inst_exist = True
        for instance in reductions:
            if instance["employee_id"] == employee.id:
                red_exist = True
        for instance in new_business:
            if instance["employee_id"] == employee.id:
                new_exist = True
        if not val_exist:
            no_valuation_employees.append(employee)
        if not inst_exist:
            no_instruction_employees.append(employee)
        if not red_exist:
            no_reduction_employees.append(employee)
        if not new_exist:
            no_new_business_employees.append(employee)

    context = {
        "employees": employees,
        "valuations": valuations,
        "instructions": instructions,
        "reductions": reductions,
        "new_business": new_business,
        "no_valuation_employees": no_valuation_employees,
        "no_instruction_employees": no_instruction_employees,
        "no_reduction_employees": no_reduction_employees,
        "no_new_business_employees": no_new_business_employees,
        "last_valuations": last_valuations,
        "last_instructions": last_instructions,
        "last_reductions": last_reductions,
        "last_new_business": last_new_business,
    }

    return render(request, "home/index.html", context)


@otp_required
@login_required
def offer_board(request):
    """A view to return the offer_board page"""

    hubs = Hub.objects.filter(is_active=True)
    employees = Profile.objects.filter(
        employee_targets=True, user__is_active=True
    )

    offers = (
        Offer.objects.exclude(propertyprocess__macro_status=4)
        .exclude(propertyprocess__macro_status=5)
        .exclude(status=Offer.REJECTED)
        .exclude(status=Offer.WITHDRAWN)
        .select_related("propertyprocess", "propertyprocess__property")
    )

    hub = None
    if "hub" in request.GET:
        selected_hub = request.GET.get("hub")
        hub = Hub.objects.get(slug=selected_hub)
        offers = offers.filter(propertyprocess__hub=hub)

    user = None
    if "user" in request.GET:
        selected_user = request.GET.get("user")
        user = Profile.objects.get(id=selected_user)
        offers = offers.filter(propertyprocess__employee=user)

    offers = offers.order_by("date")

    context = {
        "hubs": hubs,
        "selected_hub": hub,
        "employees": employees,
        "selected_user": user,
        "offers": offers,
    }

    return render(request, "home/offer_board.html", context)


@otp_required
@login_required
def employee_valuation_list(request, profile_id):
    """
    An AJAX view to return all valuations in a quarter
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    quarter_and_year = quarter_and_year_calc(timezone.now())

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]

    valuations = (
        Valuation.objects.exclude(active=False)
        .filter(
            date__iso_year=year,
            date__month__gte=start_month,
            date__month__lte=end_month,
            valuer=user,
        )
        .order_by("date")
    )

    context = {"valuations": valuations, "user": user}

    data["html_modal"] = render_to_string(
        "home/includes/employee_lists/valuation.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def employee_instruction_list(request, profile_id):
    """
    An AJAX view to return all instructions in a quarter
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    quarter_and_year = quarter_and_year_calc(timezone.now())

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]

    instructions = (
        Instruction.objects.exclude(active=False)
        .filter(
            date__iso_year=year,
            date__month__gte=start_month,
            date__month__lte=end_month,
            propertyprocess__employee=user,
        )
        .order_by("date")
    )

    context = {"instructions": instructions, "user": user}

    data["html_modal"] = render_to_string(
        "home/includes/employee_lists/instruction.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def employee_reduction_list(request, profile_id):
    """
    An AJAX view to return all reductions in a quarter
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    quarter_and_year = quarter_and_year_calc(timezone.now())

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]

    reductions = Reduction.objects.filter(
        date__iso_year=year,
        date__month__gte=start_month,
        date__month__lte=end_month,
        propertyprocess__employee=user,
    ).order_by("date")

    context = {"reductions": reductions, "user": user}

    data["html_modal"] = render_to_string(
        "home/includes/employee_lists/reduction.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def employee_new_business_list(request, profile_id):
    """
    An AJAX view to return all new business in a quarter
    """

    data = dict()

    user = Profile.objects.get(id=profile_id)

    quarter_and_year = quarter_and_year_calc(timezone.now())

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]

    new_business = PropertyFees.objects.filter(
        date__iso_year=year,
        date__month__gte=start_month,
        date__month__lte=end_month,
        propertyprocess__employee=user,
        active=True,
        show_all=True,
    ).order_by("date")

    context = {"new_business": new_business, "user": user}

    data["html_modal"] = render_to_string(
        "home/includes/employee_lists/new_business.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def deal_progression_overview(request):
    """
    A view to render the progression overview.
    """

    sector = PropertyProcess.SALES

    if request.GET:
        if "sector" in request.GET:
            sector = request.GET["sector"]

    properties_list = (
        PropertyProcess.objects.filter(macro_status=4, sector=sector)
        .select_related(
            "property",
            "deal",
        )
        .order_by("deal__date")
    )

    users = Profile.objects.filter(user__is_active=True)

    query = None
    hub = None
    user = None

    if request.GET:
        if "hub" in request.GET:
            hub = request.GET.get("hub")
            hub = Hub.objects.get(slug=hub)
            properties_list = properties_list.filter(hub=hub)

        if "query" in request.GET:
            query = request.GET["query"]
            if not query:
                return redirect(reverse("home:deal_progression_overview"))

            queries = (
                Q(property__postcode__icontains=query)
                | Q(property__address_line_1__icontains=query)
                | Q(property__address_line_2__icontains=query)
            )
            properties_list = properties_list.filter(queries)

        if "user" in request.GET:
            user = request.GET.get("user")
            user = Profile.objects.get(id=user)
            if sector == PropertyProcess.SALES:
                properties_list = properties_list.filter(
                    sales_progression__primary_progressor=user
                )
            elif sector == PropertyProcess.LETTINGS:
                properties_list = properties_list.filter(
                    lettings_progression__primary_progressor=user
                )

    properties_list_length = len(properties_list)

    page = request.GET.get("page", 1)

    paginator = Paginator(properties_list, 10)
    last_page = paginator.num_pages

    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    percentages = []

    for instance in properties:
        percentage_instance = {}
        percentage_instance["id"] = instance.id

        if sector == PropertyProcess.SALES:
            perc_calc = sales_progression_percentage(instance.id)
            percentage_instance["progression"] = perc_calc
        elif sector == PropertyProcess.LETTINGS:
            perc_calc = lettings_progression_percentage(instance.id)
            percentage_instance["progression"] = perc_calc

        percentages.append(percentage_instance)

    context = {
        "percentages": percentages,
        "properties": properties,
        "last_page": last_page,
        "properties_length": properties_list_length,
        "query": query,
        "sector": sector,
        "hub": hub,
        "users": users,
        "selected_user": user,
    }

    template = "home/progression_overview.html"

    return render(request, template, context)


@otp_required
@login_required
def add_primary_processor(request, propertyprocess_id):
    """
    A view to return an ajax response with adding property processor
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    sales_progression = get_object_or_404(
        SalesProgression, propertyprocess=property_process
    )

    if request.method == "POST":
        form = ProgressorForm(request.POST, instance=sales_progression)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
    else:
        form = ProgressorForm(instance=sales_progression)

    context = {
        "form": form,
        "property_process": property_process,
    }
    data["html_modal"] = render_to_string(
        "home/includes/progression/progressor_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def lettings_add_primary_processor(request, propertyprocess_id):
    """
    A view to return an ajax response with adding property processor
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    lettings_progression = get_object_or_404(
        LettingsProgression, propertyprocess=property_process
    )

    if request.method == "POST":
        form = LettingsProgressorForm(
            request.POST, instance=lettings_progression
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
    else:
        form = ProgressorForm(instance=lettings_progression)

    context = {
        "form": form,
        "property_process": property_process,
    }
    data["html_modal"] = render_to_string(
        "home/includes/progression/lettings_progressor_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)
