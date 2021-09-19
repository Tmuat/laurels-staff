import datetime

from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string

from lettings.forms import MaintenanceForm, MaintenanceNotesForm, EPCForm, ElectricalForm, GasForm, RenewalDateForm
from lettings.models import LettingProperties, Maintenance, MaintenanceNotes
from properties.forms import RenewalForm
from properties.models import PropertyProcess


@otp_required
@login_required
def managed_properites(request):
    """
    A view to return all managed properties.
    """

    managed_properties_list = (
        LettingProperties.objects
        .exclude(lettings_service_level="intro_only")
        .order_by(
            "propertyprocess__exchange_and_move__exchange_and_move_lettings__move_in_date"
        )
    )

    active = True
    query = None

    if request.GET:
        if "active" in request.GET:
            active = request.GET["active"]
            if active == "true":
                active = True
            elif active == "false":
                active = False

        managed_properties_list = managed_properties_list.filter(
            is_active=active
        )

        if "query" in request.GET:
            query = request.GET["query"]
            if not query:
                return redirect(reverse("home:deal_progression_overview"))

            queries = (
                Q(propertyprocess__property__postcode__icontains=query)
                | Q(propertyprocess__property__address_line_1__icontains=query)
                | Q(propertyprocess__property__address_line_2__icontains=query)
            )
            managed_properties_list = managed_properties_list.filter(queries)

    managed_properties_list_length = len(managed_properties_list)

    page = request.GET.get("page", 1)

    paginator = Paginator(managed_properties_list, 10)
    last_page = paginator.num_pages

    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        "managed_properties": properties,
        "last_page": last_page,
        "properties_length": managed_properties_list_length,
        "query": query,
        "active": active,
    }

    template = "lettings/managed_properties.html"

    return render(request, template, context)


@otp_required
@login_required
def managed_inactive(request, lettings_id):
    """
    A view to display a form to allow a property to be made inactive.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    if request.method == "POST":
        active = request.POST.get("active-selection")
        if active == "False":
            active = False
        else:
            active = True
        managed_property.is_active = active
        managed_property.save()
        data["form_is_valid"] = True
    else:
        active = request.GET.get("active")

    context = {
        "managed_property": managed_property,
        "active": active,
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/active_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def show_letting(request, lettings_id):
    """
    A view to display all information on a letting.
    """
    letting = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    context = {
        "letting": letting,
    }

    template = "lettings/letting_detail.html"

    return render(request, template, context)


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


@otp_required
@login_required
def add_epc(request, lettings_id):
    """
    A view to display a form to add EPC.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    url = reverse(
        "lettings:add_epc",
        kwargs={
            "lettings_id": managed_property.id,
        },
    )

    if request.method == "POST":
        form = EPCForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.lettings_properties = managed_property

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = EPCForm()

    context = {
        "form": form,
        "managed_property": managed_property,
        "url": url
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/add_certificate_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def add_gas(request, lettings_id):
    """
    A view to display a form to add Gas.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    url = reverse(
        "lettings:add_gas",
        kwargs={
            "lettings_id": managed_property.id,
        },
    )

    if request.method == "POST":
        form = GasForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.lettings_properties = managed_property

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = GasForm()

    context = {
        "form": form,
        "managed_property": managed_property,
        "url": url
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/add_certificate_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def add_electrical(request, lettings_id):
    """
    A view to display a form to add electrical.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    url = reverse(
        "lettings:add_electrical",
        kwargs={
            "lettings_id": managed_property.id,
        },
    )

    if request.method == "POST":
        form = ElectricalForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.lettings_properties = managed_property

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = ElectricalForm()

    context = {
        "form": form,
        "managed_property": managed_property,
        "url": url
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/add_certificate_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def add_renewal(request, lettings_id):
    """
    Add a lettings renewal.
    """

    data = dict()

    managed_property = get_object_or_404(
        LettingProperties, id=lettings_id
    )

    property_process = get_object_or_404(
        PropertyProcess, id=managed_property.propertyprocess.id
    )

    if request.method == "POST":
        form = RenewalForm(request.POST)
        renewal_form = RenewalDateForm(request.POST)
        if form.is_valid() and renewal_form.is_valid():
            instance = form.save(commit=False)
            second_instance = renewal_form.save(commit=False)

            instance.propertyprocess = property_process
            instance.active = True
            instance.show_all = False
            instance.updated_by = request.user.get_full_name()

            second_instance.lettings_properties = managed_property
            second_instance.renewed_on = form.cleaned_data["date"]
            second_instance.created_by = request.user.get_full_name()
            second_instance.updated_by = request.user.get_full_name()

            instance.save()

            second_instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = RenewalForm(
            initial={
                "fee": float(property_process.property_fees.first().fee),
                "price": float(property_process.property_fees.first().price),
                "date": datetime.date.today(),
            }
        )
        renewal_form = RenewalDateForm()

    context = {
        "form": form,
        "renewal_form": renewal_form,
        "managed_property": managed_property,
    }
    data["html_modal"] = render_to_string(
        "lettings/includes/managed/add_renewal_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def maintenance_board(request):
    """A view to return the maintenance page"""

    maintenance = (
        Maintenance.objects
        .exclude(status="completed")
        .exclude(status="cancelled")
    )

    today = datetime.date.today()

    time_since = []

    for instance in maintenance:
        data = {}
        data["id"] = instance.id
        date_created = instance.created.date()
        delta = today-date_created
        data["time_since"] = delta.days
        time_since.append(data)

    context = {
        "maintenance": maintenance,
        "time_since": time_since,
        "today": today
    }

    return render(request, "lettings/maintenance_board.html", context)
