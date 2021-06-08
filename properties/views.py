from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string

from common.functions import (
    macro_status_calculator,
    sales_progression_percentage,
)
from properties.forms import (
    PropertyForm
)
from properties.models import (
    Property,
    PropertyProcess,
    PropertyHistory,
    Offer,
    OffererDetails,
    PropertyChain,
)


def property_list(request):
    """
    A view to show paginated lists of the properties in the system; including
    searching and filtering.
    """

    properties_list = (
        PropertyProcess.objects.all()
        .select_related(
            "property",
        )
        .prefetch_related(
            "employee",
            "hub",
            "history",
        )
    )
    query = None
    status = None
    sector = None

    if request.GET:
        if "status" in request.GET:
            status = request.GET["status"]
            properties_list = properties_list.exclude(
                macro_status="comp"
            ).exclude(macro_status="withd")
        if "sector" in request.GET:
            sector = request.GET["sector"]
            properties_list = properties_list.filter(sector=sector)
        if "query" in request.GET:
            query = request.GET["query"]
            if not query:
                return redirect(reverse("properties:property_list"))

            queries = Q(property__postcode__icontains=query) | Q(
                property__address_line_1__icontains=query
            )
            properties_list = properties_list.filter(queries)

    properties_list_length = len(properties_list)

    page = request.GET.get("page", 1)

    paginator = Paginator(properties_list, 12)
    last_page = paginator.num_pages

    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        "properties": properties,
        "last_page": last_page,
        "properties_length": properties_list_length,
        "query": query,
        "status": status,
        "sector": sector,
    }

    template = "properties/property_list.html"

    return render(request, template, context)


def property_detail(request, propertyprocess_id):
    """
    A view to show individual property details
    """

    percentages = None
    property_chain = None

    propertyprocess = get_object_or_404(PropertyProcess, id=propertyprocess_id)
    property_history = propertyprocess.history.all()
    offers = propertyprocess.offerer_details.all()

    status_integer = macro_status_calculator(propertyprocess.macro_status)

    if (
        status_integer > 3
        and status_integer < 6
        and propertyprocess.sector == "sales"
    ):
        percentages = sales_progression_percentage(propertyprocess.id)
        property_chain = (
            propertyprocess.sales_progression.sales_progression_chain.all()
        )

    property_history_list_length = len(property_history)
    offers_length = len(offers)

    history_page = 1
    offer_page = 1

    history_paginator = Paginator(property_history, 5)
    offers_paginator = Paginator(offers, 6)

    history_last_page = history_paginator.num_pages
    offers_last_page = offers_paginator.num_pages

    try:
        property_history = history_paginator.page(history_page)
        offers = offers_paginator.page(offer_page)
    except PageNotAnInteger:
        property_history = history_paginator.page(1)
        offers = offers_paginator.page(1)
    except EmptyPage:
        property_history = history_paginator.page(history_paginator.num_pages)
        offers = offers_paginator.page(offers_paginator.num_pages)

    context = {
        "propertyprocess": propertyprocess,
        "property_history": property_history,
        "property_history_length": property_history_list_length,
        "history_last_page": history_last_page,
        "offers": offers,
        "offers_length": offers_length,
        "offers_last_page": offers_last_page,
        "status_integer": status_integer,
        "percentages": percentages,
        "property_chain": property_chain,
    }

    template = "properties/property_detail.html"

    return render(request, template, context)


def property_history_pagination(request, propertyprocess_id):
    """
    A view to return an ajax response with property history instance
    """

    data = dict()
    propertyprocess = get_object_or_404(PropertyProcess, id=propertyprocess_id)
    property_history = propertyprocess.history.all()

    property_history_list_length = len(property_history)

    history_page = request.GET.get("page", 1)

    history_paginator = Paginator(property_history, 5)
    history_last_page = history_paginator.num_pages

    try:
        property_history = history_paginator.page(history_page)
    except PageNotAnInteger:
        property_history = history_paginator.page(1)
    except EmptyPage:
        property_history = history_paginator.page(history_paginator.num_pages)

    context = {
        "propertyprocess": propertyprocess,
        "property_history": property_history,
        "property_history_length": property_history_list_length,
        "history_last_page": history_last_page,
    }
    data["pagination"] = render_to_string(
        "properties/includes/detail_tabs/property_history_pagination.html",
        context,
        request=request,
    )
    data["html_table"] = render_to_string(
        "properties/includes/detail_tabs/history_table.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def offers_pagination(request, propertyprocess_id):
    """
    A view to return an ajax response with offers instance
    """
    data = dict()

    propertyprocess = get_object_or_404(PropertyProcess, id=propertyprocess_id)
    offers = propertyprocess.offerer_details.all()

    offers_length = len(offers)

    offer_page = request.GET.get("page", 1)

    offers_paginator = Paginator(offers, 6)

    offers_last_page = offers_paginator.num_pages

    try:
        offers = offers_paginator.page(offer_page)
    except PageNotAnInteger:
        offers = offers_paginator.page(1)
    except EmptyPage:
        offers = offers_paginator.page(offers_paginator.num_pages)

    context = {
        "propertyprocess": propertyprocess,
        "offers": offers,
        "offers_length": offers_length,
        "offers_last_page": offers_last_page,
    }

    data["pagination"] = render_to_string(
        "properties/includes/detail_tabs/offers_pagination.html",
        context,
        request=request,
    )
    data["html_table"] = render_to_string(
        "properties/includes/detail_tabs/offer_table.html",
        context,
        request=request,
    )

    return JsonResponse(data)


def property_history_detail(request, property_history_id):
    """
    A view to return an ajax response with property history instance
    """

    data = dict()
    history_instance = get_object_or_404(
        PropertyHistory, id=property_history_id
    )

    context = {"history_instance": history_instance.notes}
    data["html_modal"] = render_to_string(
        "properties/includes/detail_tabs/property_history.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def offer_history(request, offerer_id):
    """
    A view to return an ajax response with offerer offer history
    """

    data = dict()

    offerer = get_object_or_404(OffererDetails, pk=offerer_id)
    offers = Offer.objects.filter(offerer_details=offerer_id).order_by("-date")

    context = {"offers": offers, "offerer": offerer}

    data["html_modal"] = render_to_string(
        "properties/includes/detail_tabs/offer_history.html",
        context,
        request=request,
    )

    return JsonResponse(data)


def save_property_order(request):
    data = dict()

    if request.method == "POST":
        order = request.POST.get("order")
        pk_split = order.split(",")

        for idx, pk in enumerate(pk_split):
            instance = PropertyChain.objects.get(pk=pk)
            instance.order = idx + 1
            instance.save()

        data["valid"] = True

    return JsonResponse(data)


def property_chain_detail(request, property_chain_id):
    """
    A view to return an ajax response with property chain instance
    """

    data = dict()
    chain_instance = get_object_or_404(PropertyChain, id=property_chain_id)

    context = {"instance": chain_instance}
    data["html_modal"] = render_to_string(
        "properties/includes/detail/property_chain_detail.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_property_and_valuation(request):
    """
    A view to return an ajax response with add property & valuation form
    """

    data = dict()

    form = PropertyForm()
    get_address_api_key = settings.GET_ADDRESS_KEY

    context = {"form": form, "get_address_api_key": get_address_api_key}
    data["html_modal"] = render_to_string(
        "properties/stages/add_property_and_valuation_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def validate_property_address(request):
    """
    Check that the property is not already in the database
    """
    data = dict()

    address_line_1 = request.GET.get("address_line_1", None)
    address_line_2 = request.GET.get("address_line_2", None)
    postcode = request.GET.get("postcode", None)

    context = {}
    data["html_alert"] = render_to_string(
        "properties/stages/includes/property_in_system.html",
        context,
        request=request,
    )

    data["is_taken"] = Property.objects.filter(
            address_line_1__iexact=address_line_1,
            address_line_2__iexact=address_line_2,
            postcode__iexact=postcode).exists()

    return JsonResponse(data)
