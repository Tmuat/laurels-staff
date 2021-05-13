from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.text import slugify

from common.functions import quarter_year_calc
from regionandhub.forms import (
    RegionForm,
    RegionEditForm,
    HubForm,
    HubEditForm,
    HubTargetsFormset,
)
from regionandhub.models import Region, Hub, HubTargets, HubTargetsYear


@staff_member_required
@otp_required
@login_required
def hub_and_region(request):
    """A view to return the list screen for hub and region page"""

    regions = Region.objects.filter(is_active=True).prefetch_related("region")

    current_year = quarter_year_calc()

    next_year = str(int(current_year) + 1)

    context = {
        "regions": regions,
        "current_year": current_year,
        "next_year": next_year,
    }

    template = "regionandhub/management.html"

    return render(request, template, context)


@staff_member_required
@otp_required
@login_required
def region_add(request):
    """
    Ajax URL for adding a region.
    """
    data = dict()

    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            region_name = request.POST.get("name")

            instance.slug = slugify(region_name)
            instance.is_active = True
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

            current_year = quarter_year_calc()
            next_year = str(int(current_year) + 1)

            regions = Region.objects.filter(is_active=True).prefetch_related(
                "region"
            )
            data["html_region_panels"] = render_to_string(
                "regionandhub/includes/panel.html", {
                    "regions": regions,
                    "current_year": current_year,
                    "next_year": next_year,
                }
            )
            data["html_region_page_title"] = render_to_string(
                "regionandhub/includes/page-title.html", {"regions": regions}
            )
        else:
            data["form_is_valid"] = False

    else:
        form = RegionForm()

    context = {"form": form}
    data["html_modal"] = render_to_string(
        "regionandhub/includes/add_region.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def validate_region_name(request):
    """
    Check that the region name is unique prior to form submission
    """
    region_name = request.GET.get("region_name", None)
    region_slug = slugify(region_name)
    data = {
        "is_taken": Region.objects.filter(slug__iexact=region_slug).exists()
    }
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def region_edit(request, region_slug):
    """
    Ajax URL for editing a region.
    """
    data = dict()
    region = get_object_or_404(Region, slug=region_slug)

    if request.method == "POST":
        form = RegionEditForm(request.POST, instance=region)
        if form.is_valid():
            instance = form.save(commit=False)
            region_name = request.POST.get("name")

            instance.slug = slugify(region_name)
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        form = RegionEditForm(instance=region)

    context = {"form": form, "region": region}
    data["html_modal"] = render_to_string(
        "regionandhub/includes/edit_region.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def validate_region_name_edit(request, region_slug):
    """
    Check that the region name is unique prior to
    form submission whilst editing the region.
    """
    current_slug = region_slug
    new_region_name = request.GET.get("region_name", None)
    new_region_slug = slugify(new_region_name)

    if new_region_slug == current_slug:
        data = {"is_taken": False}
    else:
        data = {
            "is_taken": Region.objects.filter(
                slug__iexact=new_region_slug
            ).exists()
        }

    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def check_region_hubs(request, region_slug):
    """
    Check that the region has no associated hubs
    before making it inactive.
    """
    region = get_object_or_404(Region, slug=region_slug)

    region.region.all().count()

    if region.region.all().count() > 0:
        data = {"associated_hubs": True}
    else:
        data = {"associated_hubs": False}

    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def hub_add(request):
    """
    Ajax URL for adding a hub.
    """
    data = dict()

    if request.method == "POST":
        form = HubForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            hub_name = request.POST.get("hub_name")

            instance.slug = slugify(hub_name)
            instance.is_active = True
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

            current_year = quarter_year_calc()
            next_year = str(int(current_year) + 1)
            
            regions = Region.objects.filter(is_active=True).prefetch_related(
                "region"
            )
            data["html_region_panels"] = render_to_string(
                "regionandhub/includes/panel.html", {
                    "regions": regions,
                    "current_year": current_year,
                    "next_year": next_year,
                }
            )
            data["html_region_page_title"] = render_to_string(
                "regionandhub/includes/page-title.html", {"regions": regions}
            )
            data["hub_slug"] = instance.slug
        else:
            data["form_is_valid"] = False

    else:
        form = HubForm()

    context = {"form": form}
    data["html_modal"] = render_to_string(
        "regionandhub/includes/add_hub.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def validate_hub_name(request):
    """
    Check that the hub name is unique prior to form submission
    """
    hub_name = request.GET.get("hub_name", None)
    hub_slug = slugify(hub_name)
    data = {"is_taken": Hub.objects.filter(slug__iexact=hub_slug).exists()}
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def hub_edit(request, hub_slug):
    """
    Ajax URL for editing a hub.
    """
    data = dict()
    hub = get_object_or_404(Hub, slug=hub_slug)

    if request.method == "POST":
        form = HubEditForm(request.POST, instance=hub)
        if form.is_valid():
            instance = form.save(commit=False)
            hub_name = request.POST.get("hub_name")

            instance.slug = slugify(hub_name)
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        form = HubEditForm(instance=hub)

    context = {"form": form, "hub": hub}
    data["html_modal"] = render_to_string(
        "regionandhub/includes/edit_hub.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def validate_hub_name_edit(request, hub_slug):
    """
    Check that the hub name is unique prior to
    form submission whilst editing the hub.
    """
    current_slug = hub_slug
    new_hub_name = request.GET.get("hub_name", None)
    new_hub_slug = slugify(new_hub_name)

    if new_hub_slug == current_slug:
        data = {"is_taken": False}
    else:
        data = {
            "is_taken": Hub.objects.filter(slug__iexact=new_hub_slug).exists()
        }

    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def hub_add_targets(request, hub):
    """
    Ajax URL for adding hub targets.
    """
    data = dict()
    hub_instance = get_object_or_404(Hub, slug=hub)
    data["hub_slug"] = hub_instance.slug

    if request.method == "POST":
        formset = HubTargetsFormset(
            request.POST, request.FILES, instance=hub_instance
        )
        selected_year = request.POST.get("year")
        if formset.is_valid():
            instances = formset.save(commit=False)
            for count, instance in enumerate(instances):
                instance.year = selected_year
                quarter = count + 1
                instance.quarter = f"q{quarter}"
                instance.created_by = request.user.get_full_name()
                instance.updated_by = request.user.get_full_name()
                instance.save()
            HubTargetsYear.objects.create(
                year=selected_year,
                targets_set=True,
                hub=hub_instance,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
            context = {"formset": formset, "hub": hub_instance}
            data["html_large_modal"] = render_to_string(
                "regionandhub/includes/add_hub_targets.html",
                context,
                request=request,
            )
    else:
        formset = HubTargetsFormset(instance=hub_instance)
        context = {"formset": formset, "hub": hub_instance}
        data["html_large_modal"] = render_to_string(
            "regionandhub/includes/add_hub_targets.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def hub_edit_targets(request, hub_slug, year):
    """
    Ajax URL for editing hub targets by year.
    """
    data = dict()
    hub_instance = get_object_or_404(Hub, slug=hub_slug)
    
    if request.method == "POST":
        formset = HubTargetsFormset(
            request.POST, request.FILES, instance=hub_instance
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.updated_by = request.user.get_full_name()
                instance.save()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        formset = HubTargetsFormset(
            instance=hub_instance,
            queryset=HubTargets.objects.filter(year=year)
        )
        context = {
            "formset": formset,
            "hub": hub_instance,
            "year": year
        }
        data["html_large_modal"] = render_to_string(
            "regionandhub/includes/edit_hub_targets.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def hub_add_specific_targets(request, hub_slug, year):
    """
    Ajax URL for adding hub targets by year.
    """
    data = dict()
    hub_instance = get_object_or_404(Hub, slug=hub_slug)
    
    if request.method == "POST":
        formset = HubTargetsFormset(
            request.POST, request.FILES, instance=hub_instance
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            for count, instance in enumerate(instances):
                instance.year = year
                quarter = count + 1
                instance.quarter = f"q{quarter}"
                instance.created_by = request.user.get_full_name()
                instance.updated_by = request.user.get_full_name()
                instance.save()
            HubTargetsYear.objects.create(
                year=year,
                targets_set=True,
                hub=hub_instance,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        formset = HubTargetsFormset(
            instance=hub_instance,
            queryset=HubTargets.objects.filter(year=year)
        )
        context = {
            "formset": formset,
            "hub": hub_instance,
            "year": year
        }
        data["html_large_modal"] = render_to_string(
            "regionandhub/includes/add_specific_hub_targets.html",
            context,
            request=request,
        )

    return JsonResponse(data)
