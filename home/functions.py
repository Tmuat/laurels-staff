from django.db.models import Count, Sum
from django.utils import timezone

from common.functions import (
    quarter_and_year_calc,
    last_quarter_and_year_calc,
)
from home.models import LastQuarterLeaderboard
from properties.models import (
    PropertyFees,
    Instruction,
    Reduction,
    Valuation,
)
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


def refresh_top_performers(request):

    refreshed_data = top_performers(timezone.now())

    bulk_create = []

    for type in refreshed_data:
        leaderboard_instance = refreshed_data[type]
        for instance in leaderboard_instance:
            count=None
            employee=None
            target=None

            for k, v in instance.items():

                if "count" in k or "sum" in k:
                    count = v
                elif "employee" in k:
                    employee = Profile.objects.get(id=v)
                elif "target" in k:
                    target = v
                
            bulk_create.append(
                LastQuarterLeaderboard(
                    type=f"{type}",
                    employee=employee,
                    count=count,
                    target_percentage=target,
                    updated_by=request.user.get_full_name()
                )
            )

    LastQuarterLeaderboard.objects.all().delete()
    LastQuarterLeaderboard.objects.bulk_create(
        bulk_create
    )

    return refreshed_data
