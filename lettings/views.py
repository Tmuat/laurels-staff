from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string

from lettings.forms import MaintenanceForm, MaintenanceNotesForm
from lettings.models import LettingProperties, Maintenance, MaintenanceNotes


@otp_required
@login_required
def show_maintenance(request, lettings_id):
    """
    A view to display all maintenance for a given property.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    maintenance_qs = Maintenance.objects.filter(
        lettings_properties=managed_property
    )

    context = {
        "managed_property": managed_property,
        "maintenance_qs": maintenance_qs,
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/maintenance_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def view_maintenance(request, maintenance_id):
    """
    A view to show all the detail of a maintenance object.
    """

    maintenance = get_object_or_404(
        Maintenance, id=maintenance_id
    )

    context = {
        "maintenance": maintenance,
    }

    template = "lettings/maintenance_detail.html"

    return render(request, template, context)


@otp_required
@login_required
def add_maintenance(request, lettings_id):
    """
    A view to display a form to add maintenance.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    url = reverse(
        "lettings:add_maintenance",
        kwargs={
            "lettings_id": managed_property.id,
        },
    )

    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.lettings_properties = managed_property

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            notes = (
                "A maintenance was added by "
                f"{request.user.get_full_name()}."
            )

            instance.save()

            MaintenanceNotes.objects.create(
                maintenance=instance,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name()
            )

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = MaintenanceForm()

    context = {
        "form": form,
        "managed_property": managed_property,
        "url": url
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/add_maintenance_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def edit_maintenance(request, lettings_id, maintenance_id):
    """
    A view to display a form to edit maintenance.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    maintenance = get_object_or_404(
        Maintenance, id=maintenance_id
    )

    url = reverse(
        "lettings:edit_maintenance",
        kwargs={
            "lettings_id": managed_property.id,
            "maintenance_id": maintenance.id,
        },
    )

    if request.method == "POST":
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = MaintenanceForm(instance=maintenance)

    context = {
        "form": form,
        "managed_property": managed_property,
        "url": url
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/add_maintenance_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def add_maintenance_note(request, maintenance_id):
    """
    A view to display a form to add maintenance note.
    """

    data = dict()

    maintenance = get_object_or_404(
        Maintenance, id=maintenance_id
    )

    if request.method == "POST":
        form = MaintenanceNotesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.maintenance = maintenance

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = MaintenanceNotesForm()

    context = {
        "form": form,
        "maintenance": maintenance,
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/add_maintenance_notes_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)
