import datetime

from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone

from common.functions import quarter_and_year_calc
from properties.models import (
    Offer, PropertyFees, Instruction, Reduction, Valuation
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

    quarter_and_year = quarter_and_year_calc(timezone.now())

    year = quarter_and_year["start_year"]
    start_month = quarter_and_year["start_month"]
    end_month = quarter_and_year["end_month"]
    quarter = quarter_and_year["quarter"]
    company_year = quarter_and_year["company_year"]

    employee = "propertyprocess__employee__id"
    link_to_employee = 'propertyprocess__employee'
    reductions = 'propertyprocess__employee'

    valuations = Valuation.objects.values("valuer") \
        .annotate(valuation_count=Count(link_to_employee)) \
        .filter(date__iso_year=year,
                date__month__gte=start_month,
                date__month__lte=end_month,
                propertyprocess__employee__employee_targets=True,
                propertyprocess__employee__user__is_active=True) \
        .order_by('-valuation_count')

    instructions = Instruction.objects.values(employee) \
        .annotate(instruction_count=Count(link_to_employee)) \
        .filter(date__iso_year=year,
                date__month__gte=start_month,
                date__month__lte=end_month,
                propertyprocess__employee__employee_targets=True,
                propertyprocess__employee__user__is_active=True) \
        .order_by('-instruction_count')

    reductions = Reduction.objects.values(employee) \
        .annotate(reduction_count=Count(link_to_employee)) \
        .filter(date__iso_year=year,
                date__month__gte=start_month,
                date__month__lte=end_month,
                propertyprocess__employee__employee_targets=True,
                propertyprocess__employee__user__is_active=True) \
        .order_by('-reduction_count')

    new_business = PropertyFees.objects.values(employee) \
        .annotate(new_business_sum=Sum('new_business')) \
        .filter(date__iso_year=year,
                date__month__gte=start_month,
                date__month__lte=end_month,
                propertyprocess__employee__employee_targets=True,
                propertyprocess__employee__user__is_active=True,
                active=True,
                show_all=True) \
        .order_by('-new_business_sum')

    targets = UserTargets.objects.filter(
        year=company_year,
        quarter=quarter
    )

    # Renaming fields in querysets
    for instance in valuations:
        instance["employee_id"] = instance[
            "valuer"
        ]
        del instance["valuer"]

        instance["valuation_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                valuation_target = round(instance[
                    "valuation_count"
                ] / target.valuations, 2) * 100
                instance["valuation_target"] = valuation_target

    for instance in instructions:
        instance["employee_id"] = instance[
            "propertyprocess__employee__id"
        ]
        del instance["propertyprocess__employee__id"]

        instance["instruction_target"] = 0

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

        instance["reduction_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                reduction_target = round(instance[
                    "reduction_count"
                ] / target.reductions, 2) * 100
                instance["reduction_target"] = reduction_target

    for instance in new_business:
        instance["employee_id"] = instance[
            "propertyprocess__employee__id"
        ]
        del instance["propertyprocess__employee__id"]

        instance["new_business_target"] = 0

        for target in targets:
            if instance["employee_id"] == target.profile_targets.id:
                new_business_target = round(instance[
                    "new_business_sum"
                ] / target.new_business, 2) * 100
                instance["new_business_target"] = new_business_target

    valuations = sorted(
        valuations,
        key=lambda k: k['valuation_target'],
        reverse=True
    )

    instructions = sorted(
        instructions,
        key=lambda k: k['instruction_target'],
        reverse=True
    )

    reductions = sorted(
        reductions,
        key=lambda k: k['reduction_target'],
        reverse=True
    )

    new_business = sorted(
        new_business,
        key=lambda k: k['new_business_target'],
        reverse=True
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
