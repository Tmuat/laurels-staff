from django_otp.decorators import otp_required

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string

from common.decorators import director_required
from touts.forms import (
    AreaForm,
    AreaEditForm,
    AddPropertyForm,
    AddLandlordForm,
    AddLandlordExistingPropertyForm,
    AddMarketingForm,
    AddMarketingExistingLandlordForm,
    ToutLetterFormSet
)
from touts.models import (
    Area,
    ToutProperty,
    Landlord,
    ToutLetter,
)


@director_required
@staff_member_required
@otp_required
@login_required
def area_list(request):
    """
    A view to show paginated lists of all touting areas in the system;
    including searching and filtering.
    """

    area_list = Area.objects.all()

    active = True

    if request.GET:
        if "active" in request.GET:
            active = request.GET["active"]
            if active == "True":
                active = True
            elif active == "False":
                active = False

    if active is True:
        area_list = area_list.filter(is_active=True)

    page = request.GET.get("page", 1)

    paginator = Paginator(area_list, 16)
    last_page = paginator.num_pages

    try:
        area_list = paginator.page(page)
    except PageNotAnInteger:
        area_list = paginator.page(1)
    except EmptyPage:
        area_list = paginator.page(paginator.num_pages)

    context = {
        "area_list": area_list,
        "active": active,
        "last_page": last_page,
    }

    template = "touts/area_list.html"

    return render(request, template, context)


@director_required
@staff_member_required
@otp_required
@login_required
def area_add(request):
    """
    Ajax URL for adding an area.
    """
    data = dict()

    if request.method == "POST":
        form = AreaForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.is_active = True
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        form = AreaForm()

    context = {"form": form}
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_area.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@director_required
@staff_member_required
@otp_required
@login_required
def area_edit(request, area_code):
    """
    Ajax URL for editing an area.
    """
    data = dict()

    area_code = get_object_or_404(Area, area_code=area_code)

    if request.method == "POST":
        form = AreaEditForm(request.POST, instance=area_code)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        form = AreaEditForm(instance=area_code)

    context = {
        "form": form,
        "instance": area_code
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/edit_area.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@director_required
@staff_member_required
@otp_required
@login_required
def validate_area_code(request):
    """
    Check that the area code is unique prior to form submission
    """
    area_code = request.GET.get("area_code", None)
    print(area_code)
    data = {
        "is_taken": Area.objects.filter(area_code__iexact=area_code).exists()
    }
    return JsonResponse(data)


def tout_list_extra_data(area_list):
    """
    Used to get additional context to display the tout list correctly.
    """

    tout_list_data = []

    for area_instance in area_list:
        dict_instance = {}

        dict_instance["area_id"] = area_instance.id
        dict_instance["active_properties"] = 0
        dict_instance["inactive_properties"] = 0

        for property_instance in area_instance.area.all():
            for landlord_instance in property_instance.landlord_property.all():
                for marketing_instance in landlord_instance.landlord.all():
                    if marketing_instance.is_active is True:
                        dict_instance["active_properties"] += 1
                    else:
                        dict_instance["inactive_properties"] += 1

        tout_list_data.append(dict_instance)

    return tout_list_data


@otp_required
@login_required
def tout_list(request):
    """
    A view to show paginated lists of all touting areas and
    the properties in the system.
    """

    area_list = Area.objects.all()

    query = None
    active = None

    if "active" in request.GET:
        active = request.GET["active"]
        if active == "true":
            active = True
        else:
            active = False
    else:
        area_list = Area.objects.filter(
            is_active=True
        )

    if "query" in request.GET:
        query = request.GET["query"]
        if not query:
            return redirect(reverse("touts:tout_list"))

        queries = (
            Q(area_code__icontains=query)
        )
        area_list = area_list.filter(queries)

    extra_info = tout_list_extra_data(area_list)

    page = request.GET.get("page", 1)

    paginator = Paginator(area_list, 16)
    last_page = paginator.num_pages

    try:
        area_list = paginator.page(page)
    except PageNotAnInteger:
        area_list = paginator.page(1)
    except EmptyPage:
        area_list = paginator.page(paginator.num_pages)

    context = {
        "area_list": area_list,
        "extra_info": extra_info,
        "last_page": last_page,
        "query": query,
        "active": active
    }

    template = "touts/tout_list.html"

    return render(request, template, context)


def area_detail_extra_data(area_property_list):
    """
    Used to get additional context to display the area property
    list data correctly.
    """

    property_list_data = []

    for property_instance in area_property_list:
        dict_instance = {}

        dict_instance["property_id"] = property_instance.id
        dict_instance["property_str"] = property_instance.address
        dict_instance["landlords"] = []
        dict_instance["active_touts"] = 0
        dict_instance["inactive_touts"] = 0

        for landlord_instance in property_instance.landlord_property.all():
            landlord_dict_instance = {}
            landlord_dict_instance["landlord_id"] = landlord_instance.id
            landlord_dict_instance["landlord_name"] = landlord_instance.landlord_name
            landlord_dict_instance["landlord_salutation"] = landlord_instance.landlord_salutation
            landlord_dict_instance["active_touts"] = 0
            landlord_dict_instance["inactive_touts"] = 0
            landlord_dict_instance["touts"] = []
            landlord_dict_instance["furthest_letter"] = 0

            dict_instance["landlords"].append(landlord_dict_instance)

            active_tout = False

            for marketing_instance in landlord_instance.landlord.all():
                marketing_dict_instance = {}
                marketing_dict_instance["marketing_id"] = marketing_instance.id
                marketing_dict_instance["marketing_furthest_letter"] = marketing_instance.furthest_letter
                marketing_dict_instance["marketing_is_active"] = marketing_instance.is_active

                if marketing_instance.is_active is True:
                    dict_instance["active_touts"] += 1
                    landlord_dict_instance["active_touts"] += 1
                    active_tout = True
                else:
                    dict_instance["inactive_touts"] += 1
                    landlord_dict_instance["inactive_touts"] += 1

                landlord_dict_instance["touts"].append(marketing_dict_instance)

            if active_tout:
                for tout_instance in landlord_dict_instance["touts"]:
                    if tout_instance["marketing_is_active"] is True:
                        landlord_dict_instance["furthest_letter"] = tout_instance["marketing_furthest_letter"]

        property_list_data.append(dict_instance)

    return property_list_data


def inactive_properties(area_properties):
    """
    Checks if all properties in an area are inactive.
    """

    active_sums = 0

    for instance in area_properties:
        active_sums += instance["active_touts"]

    return active_sums


@otp_required
@login_required
def area_detail(request, area_id):
    """
    A view to show paginated lists of all tout properties for
    a specific area.
    """

    area = Area.objects.get(
        id=area_id
    )

    properties = ToutProperty.objects.filter(
        area=area.id
    )

    query = None
    active = None

    if "active" in request.GET:
        active = request.GET["active"]
        if active == "true":
            active = True
        else:
            active = False

    if "query" in request.GET:
        query = request.GET["query"]
        if not query:
            return redirect(
                reverse(
                    "touts:area_detail",
                    kwargs={
                        "area_id": area.id,
                    },
                )
            )

        queries = (
            Q(postcode__icontains=query)
        )
        properties = properties.filter(queries)

    extra_info = area_detail_extra_data(properties)
    active_count = inactive_properties(extra_info)
    print(active_count)

    page = request.GET.get("page", 1)

    paginator = Paginator(extra_info, 16)
    last_page = paginator.num_pages

    try:
        extra_info = paginator.page(page)
    except PageNotAnInteger:
        extra_info = paginator.page(1)
    except EmptyPage:
        extra_info = paginator.page(paginator.num_pages)

    context = {
        "area": area,
        "properties_list": extra_info,
        "last_page": last_page,
        "query": query,
        "active": active,
        "active_count": active_count
    }

    template = "touts/area_detail.html"

    return render(request, template, context)


@otp_required
@login_required
def loud_tout_menu(request):
    """
    A view to load the tout menu.
    """

    data = dict()

    data["html_modal"] = render_to_string(
        "touts/includes/menu.html",
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def add_tout_property(request):
    """
    Ajax URL for adding a tout property.
    """
    data = dict()

    get_address_api_key = settings.GET_ADDRESS_KEY

    if request.method == "POST":
        form = AddPropertyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()
            instance.save()

            data["form_is_valid"] = True
            data["form_chain"] = True
            data["next"] = reverse(
                "touts:add_landord",
                kwargs={
                    "tout_property": instance.id,
                },
            )
        else:
            data["form_is_valid"] = False

    else:
        form = AddPropertyForm()

    context = {
        "form": form,
        "get_address_api_key": get_address_api_key,
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_tout_property.html",
        context,
        request=request,
    )
    data["modal"] = "large"
    data["selectTwo"] = True

    return JsonResponse(data)


@otp_required
@login_required
def validate_tout_property_address(request):
    """
    Check that the tout property is not already in the database
    """
    data = dict()
    instance = None

    address_line_1 = request.GET.get("address_line_1", None)
    address_line_2 = request.GET.get("address_line_2", None)
    postcode = request.GET.get("postcode", None)

    if address_line_2 == "":
        address_line_2 = None

    data["is_taken"] = ToutProperty.objects.filter(
        address_line_1__iexact=address_line_1,
        address_line_2__iexact=address_line_2,
        postcode__iexact=postcode,
    ).exists()

    if data["is_taken"] is True:
        instance = ToutProperty.objects.get(
            address_line_1__iexact=address_line_1,
            address_line_2__iexact=address_line_2,
            postcode__iexact=postcode,
        )

        context = {"instance": instance}
        data["html_alert"] = render_to_string(
            "touts/includes/alerts/property_in_system.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@otp_required
@login_required
def add_landord(request, tout_property):
    """
    Ajax URL for adding a landlord to a tout property.
    """
    data = dict()

    get_address_api_key = settings.GET_ADDRESS_KEY

    tout_property = get_object_or_404(
        ToutProperty, id=tout_property
    )

    if request.method == "POST":
        form = AddLandlordForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.landlord_property = tout_property
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()
            instance.save()

            data["form_is_valid"] = True
            data["form_chain"] = True
            data["next"] = reverse(
                "touts:add_marketing",
                kwargs={
                    "landlord": instance.id,
                },
            )
        else:
            data["form_is_valid"] = False

    else:
        form = AddLandlordForm()
        data["selectTwo"] = True

    context = {
        "form": form,
        "get_address_api_key": get_address_api_key,
        "tout_property": tout_property,
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_landlord.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def add_landord_existing_property(request):
    """
    Ajax URL for adding a landlord to a existing tout property.
    """
    data = dict()

    get_address_api_key = settings.GET_ADDRESS_KEY

    if request.method == "POST":
        form = AddLandlordExistingPropertyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()
            instance.save()

            data["form_is_valid"] = True
            data["form_chain"] = True
            data["next"] = reverse(
                "touts:add_marketing",
                kwargs={
                    "landlord": instance.id,
                },
            )
        else:
            data["form_is_valid"] = False

    else:
        form = AddLandlordExistingPropertyForm()
        data["selectTwo"] = True

    context = {
        "form": form,
        "get_address_api_key": get_address_api_key,
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_landlord_existing.html",
        context,
        request=request,
    )
    data["selectTwo"] = True
    data["modal"] = "large-static"

    return JsonResponse(data)


@otp_required
@login_required
def add_marketing(request, landlord):
    """
    Ajax URL for adding a marketing info to a landlord.
    """
    data = dict()

    landlord = get_object_or_404(
        Landlord, id=landlord
    )

    if request.method == "POST":
        if request.user.profile.director:
            form = AddMarketingForm(request.POST)
            formset = ToutLetterFormSet(
                request.POST, request.FILES
            )
            if form.is_valid() and formset.is_valid():
                instance = form.save(commit=False)
                instance.landlord = landlord
                instance.created_by = request.user.get_full_name()
                instance.updated_by = request.user.get_full_name()
                instance.save()

                for count, formset_instance in enumerate(formset):
                    form_number = count + 1
                    if formset_instance.cleaned_data["sent"] == "True":
                        ToutLetter.objects.create(
                            date=formset_instance.cleaned_data["date"],
                            letter=form_number,
                            marketing=instance,
                            created_by=request.user.get_full_name(),
                            updated_by=request.user.get_full_name()
                        )
                data["form_is_valid"] = True
            else:
                data["form_is_valid"] = False
        else:
            form = AddMarketingForm(request.POST)
            formset = ToutLetterFormSet()
            if form.is_valid():
                instance = form.save(commit=False)
                instance.landlord = landlord
                instance.created_by = request.user.get_full_name()
                instance.updated_by = request.user.get_full_name()
                instance.save()

                data["form_is_valid"] = True
            else:
                data["form_is_valid"] = False
    else:
        form = AddMarketingForm()
        formset = ToutLetterFormSet()

    context = {
        "form": form,
        "formset": formset,
        "landlord": landlord,
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_marketing.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def add_marketing_existing_landlord(request):
    """
    Ajax URL for adding marketing info to an existing landlord.
    """
    data = dict()

    if request.method == "POST":
        if request.user.profile.director:
            form = AddMarketingExistingLandlordForm(request.POST)
            formset = ToutLetterFormSet(
                request.POST, request.FILES
            )
            if form.is_valid() and formset.is_valid():
                instance = form.save(commit=False)
                instance.created_by = request.user.get_full_name()
                instance.updated_by = request.user.get_full_name()
                instance.save()

                for count, formset_instance in enumerate(formset):
                    form_number = count + 1
                    if formset_instance.cleaned_data["sent"] == "True":
                        ToutLetter.objects.create(
                            date=formset_instance.cleaned_data["date"],
                            letter=form_number,
                            marketing=instance,
                            created_by=request.user.get_full_name(),
                            updated_by=request.user.get_full_name()
                        )
                data["form_is_valid"] = True
            else:
                data["form_is_valid"] = False
        else:
            form = AddMarketingExistingLandlordForm(request.POST)
            formset = ToutLetterFormSet()
            if form.is_valid():
                instance = form.save(commit=False)
                instance.created_by = request.user.get_full_name()
                instance.updated_by = request.user.get_full_name()
                instance.save()
                data["form_is_valid"] = True
            else:
                data["form_is_valid"] = False
    else:
        form = AddMarketingExistingLandlordForm()
        formset = ToutLetterFormSet()

    context = {
        "form": form,
        "formset": formset
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_marketing_existing.html",
        context,
        request=request,
    )
    data["selectTwo"] = True
    data["modal"] = "large-static"

    return JsonResponse(data)
