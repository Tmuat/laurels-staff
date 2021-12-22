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
    AddMarketingExistingLandlordForm
)
from touts.models import Area, ToutProperty, Landlord, ToutLetter


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


@otp_required
@login_required
def tout_list(request):
    """
    A view to show paginated lists of all touting areas and the properties in the system.
    """

    area_list = Area.objects.filter(
        is_active=True
    )

    query = None
    active = None

    if request.GET:
        if "active" in request.GET:
            active = request.GET["active"]
            if active == "true":
                active = True
            else:
                active = False
            area_list = area_list.filter(
                area__landlord_property__landlord__marketing_info__do_not_send=active
            )
        if "query" in request.GET:
            query = request.GET["query"]
            if not query:
                return redirect(reverse("touts:tout_list"))

            queries = (
                Q(area__postcode__icontains=query)
                | Q(area__address_line_1__icontains=query)
                | Q(area__address_line_2__icontains=query)
            )
            area_list = area_list.filter(queries)

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
        "last_page": last_page,
        "query": query,
        "active": active
    }

    template = "touts/tout_list.html"

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
        form = AddMarketingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.landlord = landlord
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()
            instance.save()
            ToutLetter.objects.create(
                marketing=instance.id,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = AddMarketingForm()

    context = {
        "form": form,
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
        form = AddMarketingExistingLandlordForm(request.POST)
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
        form = AddMarketingExistingLandlordForm()

    context = {
        "form": form,
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_marketing_existing.html",
        context,
        request=request,
    )
    data["selectTwo"] = True
    data["modal"] = "large-static"

    return JsonResponse(data)


# @otp_required
# @login_required
# def add_marketing(request, landlord):
#     """
#     Ajax URL for adding a marketing info to a landlord.
#     """
#     data = dict()

#     landlord = get_object_or_404(
#         Landlord, id=landlord
#     )

#     if request.method == "POST":
#         form = AddMarketingForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.landlord = landlord
#             instance.created_by = request.user.get_full_name()
#             instance.updated_by = request.user.get_full_name()
#             instance.save()
#             ToutLetter.objects.create(
#                 marketing=instance.id,
#                 created_by=request.user.get_full_name(),
#                 updated_by=request.user.get_full_name(),
#             )
#             data["form_is_valid"] = True
#         else:
#             data["form_is_valid"] = False
#     else:
#         form = AddMarketingForm()

#     context = {
#         "form": form,
#         "landlord": landlord,
#     }
#     data["html_modal"] = render_to_string(
#         "touts/includes/forms/add_marketing.html",
#         context,
#         request=request,
#     )
#     return JsonResponse(data)
