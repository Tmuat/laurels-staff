from django_otp.decorators import otp_required

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from common.decorators import director_required
from common.functions import quarter_year_calc
from users.forms import UserTargetsFormset, UserForm, ProfileForm
from users.models import UserTargets, UserTargetsByYear, CustomUser


@director_required
@staff_member_required
@otp_required
@login_required
def employees(request):
    """
    A view to show paginated lists of employees.
    """

    users = (
        get_user_model()
        .objects.all()
        .order_by(
            "first_name",
        )
    )

    active = True

    if request.GET:
        if "active" in request.GET:
            active = request.GET["active"]
            if active == "True":
                active = True
            elif active == "False":
                active = False

    if active is True:
        users = users.filter(is_active=True)

    page = request.GET.get("page", 1)

    paginator = Paginator(users, 16)
    last_page = paginator.num_pages

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    current_year = quarter_year_calc()

    targets_set = []

    for user in users:
        if user.profile.employee_targets:
            user_target = {}
            user_target["pk"] = user.pk
            user_target["name"] = user.get_full_name()
            user_target["current_year"] = False
            for user_targets_year in user.user_targets_year_set.all():
                if (
                    user_targets_year.year == current_year
                    and user_targets_year.targets_set
                ):
                    user_target["current_year"] = True

            targets_set.append(user_target)

    context = {
        "users": users,
        "active": active,
        "last_page": last_page,
        "targets_set": targets_set,
        "current_year": current_year,
    }

    template = "users/employee_list_view.html"

    return render(request, template, context)


@director_required
@staff_member_required
@otp_required
@login_required
def add_user_targets(request, user, year):
    """
    Ajax URL for adding user targets.
    """
    data = dict()
    user = get_object_or_404(CustomUser, pk=user)

    if request.method == "POST":
        formset = UserTargetsFormset(
            request.POST, request.FILES, instance=user
        )
        request_user = request.user.get_full_name()
        profile = user.profile
        if formset.is_valid():
            instances = formset.save(commit=False)
            for count, instance in enumerate(instances):
                instance.year = year
                quarter = count + 1
                instance.quarter = f"q{quarter}"
                instance.profile_targets = profile
                instance.created_by = request_user
                instance.updated_by = request_user
                instance.save()
            UserTargetsByYear.objects.create(
                year=year,
                targets_set=True,
                user=user,
                profile=profile,
                created_by=request_user,
                updated_by=request_user,
            )
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
            context = {
                "formset": formset,
                "user": user,
                "year": year,
            }
            data["html_large_modal"] = render_to_string(
                "users/includes/add_user_targets.html",
                context,
                request=request,
            )
    else:
        formset = UserTargetsFormset(
            instance=user, queryset=UserTargets.objects.filter(year=year)
        )
        context = {
            "formset": formset,
            "user": user,
            "year": year,
        }
        data["html_modal"] = render_to_string(
            "users/includes/add_user_targets.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@director_required
@staff_member_required
@otp_required
@login_required
def edit_user_targets(request, user, year):
    """
    Ajax URL for editing user targets.
    """
    data = dict()
    user = get_object_or_404(CustomUser, pk=user)

    if request.method == "POST":
        formset = UserTargetsFormset(
            request.POST, request.FILES, instance=user
        )
        request_user = request.user.get_full_name()
        profile = user.profile
        if formset.is_valid():
            instances = formset.save(commit=False)
            for count, instance in enumerate(instances):
                instance.year = year
                quarter = count + 1
                instance.quarter = f"q{quarter}"
                instance.profile_targets = profile
                instance.created_by = request_user
                instance.updated_by = request_user
                instance.save()
            user_targets_by_year = get_object_or_404(
                UserTargetsByYear, user=user, year=year
            )
            user_targets_by_year.updated_by = request_user
            user_targets_by_year.save()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
            context = {
                "formset": formset,
                "user": user,
                "year": year,
            }
            data["html_large_modal"] = render_to_string(
                "users/includes/edit_user_targets.html",
                context,
                request=request,
            )
    else:
        formset = UserTargetsFormset(
            instance=user, queryset=UserTargets.objects.filter(year=year)
        )
        context = {
            "formset": formset,
            "user": user,
            "year": year,
        }
        data["html_modal"] = render_to_string(
            "users/includes/edit_user_targets.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@director_required
@staff_member_required
@otp_required
@login_required
def user_detail(request, user):
    """
    A view to render a large modal for showing user detail
    """

    data = dict()
    user = get_object_or_404(CustomUser, pk=user)

    current_year = quarter_year_calc()

    next_year = str(int(current_year) + 1)

    targets_set = []

    if user.profile.employee_targets:
        user_target = {}
        user_target["current_year"] = False
        user_target["next_year"] = False
        for user_targets_year in user.user_targets_year_set.all():
            if (
                user_targets_year.year == current_year
                and user_targets_year.targets_set
            ):
                user_target["current_year"] = True

            if (
                user_targets_year.year == next_year
                and user_targets_year.targets_set
            ):
                user_target["next_year"] = True

        targets_set.append(user_target)

    context = {
        "user": user,
        "current_year": current_year,
        "next_year": next_year,
        "targets_set": targets_set,
    }

    data["html_modal"] = render_to_string(
        "users/includes/user_expanded.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@director_required
@staff_member_required
@otp_required
@login_required
def edit_user(request, user):
    """
    Deals with editing a user and profile
    """
    data = dict()
    user = get_object_or_404(CustomUser, pk=user)

    if request.method == "POST":
        print("HERE")
        form = UserForm(
            request.POST,
            instance=user,
        )
        profile_form = ProfileForm(
            request.POST,
            instance=user.profile,
        )
        if form.is_valid() and profile_form.is_valid():
            print("NOT VALID")
            form.save()

            profile_instance = profile_form.save(commit=False)
            profile_instance.updated_by = request.user.get_full_name()
            profile_instance.save()

            for hub in profile_form.cleaned_data["hub"]:
                profile_instance.hub.add(hub)
            profile_instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

            context = {
                "form": form,
                "profile_form": profile_form,
                "user": user,
            }
            data["html_modal"] = render_to_string(
                "users/includes/edit_user.html",
                context,
                request=request,
            )
    else:
        print("GET REQUEST")
        form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        context = {
            "form": form,
            "profile_form": profile_form,
            "user": user,
        }
        data["html_modal"] = render_to_string(
            "users/includes/edit_user.html",
            context,
            request=request,
        )

    return JsonResponse(data)
