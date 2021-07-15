from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F, Q
from django.shortcuts import render

from common.functions import quarter_and_year_calc
from properties.models import (
    Offer, PropertyFees, Instruction, Reduction
)
from regionandhub.models import Hub
from users.models import Profile, UserTargets


@otp_required
@login_required
def index(request):
    """A view to return the index page"""

    employees = Profile.objects.filter(
        employee_targets=True, user__is_active=True
    )

    quarter_and_year = quarter_and_year_calc()

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]
    quarter = quarter_and_year["quarter"]

    employee = "propertyprocess__employee__id"
    name = "propertyprocess__employee__user__first_name"
    instructions = 'propertyprocess__employee'
    reductions = 'propertyprocess__employee'

    instructions = Instruction.objects.values(employee, name) \
        .annotate(instruction_count=Count(instructions)) \
        .filter(date__iso_year=year,
                date__month__gte=start_month,
                date__month__lte=end_month,
                propertyprocess__employee__employee_targets=True,
                propertyprocess__employee__user__is_active=True) \
        .order_by('-instruction_count')

    reductions = Reduction.objects.values(employee, name) \
        .annotate(reduction_count=Count(reductions)) \
        .filter(date__iso_year=year,
                date__month__gte=start_month,
                date__month__lte=end_month,
                propertyprocess__employee__employee_targets=True,
                propertyprocess__employee__user__is_active=True) \
        .order_by('-reduction_count')

    targets = UserTargets.objects.filter(
        year=year,
        quarter=quarter
    )

    # Renaming fields in querysets
    for instance in instructions:
        instance["employee_id"] = instance[
            "propertyprocess__employee__id"
        ]
        del instance["propertyprocess__employee__id"]

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                instruction_target = round(instance[
                    "instruction_count"
                ] / target.instructions, 2) * 100
                instance["instruction_target"] = instruction_target

    for instance in reductions:
        instance["employee_id"] = instance[
            "propertyprocess__employee__id"
        ]
        del instance["propertyprocess__employee__id"]

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                reduction_target = round(instance[
                    "reduction_count"
                ] / target.reductions, 2) * 100
                instance["reduction_target"] = reduction_target

    # Creating lists of employees who haven't aren't on the lists
    no_instruction_employees = []
    no_reduction_employees = []

    for employee in employees:
        inst_exist = False
        red_exist = False
        for instance in instructions:
            if instance["employee_id"] == employee.id:
                inst_exist = True
        for instance in reductions:
            if instance["employee_id"] == employee.id:
                red_exist = True
        if not inst_exist:
            no_instruction_employees.append(employee)
        if not red_exist:
            no_reduction_employees.append(employee)

    context = {
        "employees": employees,
        "instructions": instructions,
        "reductions": reductions,
        "no_instruction_employees": no_instruction_employees,
        "no_reduction_employees": no_reduction_employees,
    }

    return render(request, "home/index.html", context)


def offer_board(request):
    """A view to return the offer_board page"""

    hubs = Hub.objects.filter(is_active=True)
    employees = Profile.objects.filter(
        employee_targets=True, user__is_active=True
    )

    offers = Offer.objects.exclude(propertyprocess__macro_status=4). \
        exclude(propertyprocess__macro_status=5). \
        exclude(status=Offer.REJECTED). \
        exclude(status=Offer.WITHDRAWN). \
        select_related(
            "propertyprocess",
            "propertyprocess__property"
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
