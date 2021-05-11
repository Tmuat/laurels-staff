from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.text import slugify

from regionandhub.forms import RegionForm, HubForm
from regionandhub.models import Region, Hub


@otp_required
@login_required
def hub_and_region(request):
    """A view to return the list screen for hub and region page"""

    regions = Region.objects.filter(is_active=True).prefetch_related("region")

    context = {"regions": regions}

    template = "regionandhub/management.html"

    return render(request, template, context)


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
            regions = Region.objects.filter(is_active=True).prefetch_related(
                "region"
            )
            data["html_region_panels"] = render_to_string(
                "regionandhub/includes/panel.html", {"regions": regions}
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
            regions = Region.objects.filter(is_active=True).prefetch_related(
                "region"
            )
            data["html_region_panels"] = render_to_string(
                "regionandhub/includes/panel.html", {"regions": regions}
            )
            data["html_region_page_title"] = render_to_string(
                "regionandhub/includes/page-title.html", {"regions": regions}
            )
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
