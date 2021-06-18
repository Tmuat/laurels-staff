from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string

from common.functions import (
    sales_progression_percentage,
)
from properties.forms import (
    PropertyForm,
    PropertyProcessForm,
    ValuationForm,
    InstructionForm,
    SellerMarketingForm,
    HistoryNotesForm,
    FloorSpaceForm,
)
from properties.models import (
    Property,
    PropertyProcess,
    PropertyFees,
    PropertyHistory,
    Offer,
    OffererDetails,
    PropertyChain,
    Valuation,
)
from users.models import Profile


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
            properties_list = properties_list.exclude(macro_status=5).exclude(
                macro_status=0
            )
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

    if propertyprocess.macro_status > 3 and propertyprocess.sector == "sales":
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


def render_property(request):
    """
    A view to return an ajax response with add property form
    """

    data = dict()

    employee = Profile.objects.get(user=request.user.id)
    hub = employee.hub.first()
    instance = PropertyProcess(employee=employee, hub=hub)

    form = PropertyForm()
    process_form = PropertyProcessForm(instance=instance)
    get_address_api_key = settings.GET_ADDRESS_KEY

    context = {
        "form": form,
        "process_form": process_form,
        "get_address_api_key": get_address_api_key,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_property_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def validate_property_address(request):
    """
    Check that the property is not already in the database
    """
    data = dict()
    instance = None

    address_line_1 = request.GET.get("address_line_1", None)
    address_line_2 = request.GET.get("address_line_2", None)
    postcode = request.GET.get("postcode", None)

    if address_line_2 == "":
        address_line_2 = None

    data["is_taken"] = Property.objects.filter(
        address_line_1__iexact=address_line_1,
        address_line_2__iexact=address_line_2,
        postcode__iexact=postcode,
    ).exists()

    if data["is_taken"] is True:
        instance = Property.objects.get(
            address_line_1__iexact=address_line_1,
            address_line_2__iexact=address_line_2,
            postcode__iexact=postcode,
        )

        context = {"instance": instance}
        data["html_alert"] = render_to_string(
            "properties/stages/includes/property_in_system.html",
            context,
            request=request,
        )

    return JsonResponse(data)


def add_property(request):
    """
    Ajax URL for adding a property.
    """
    data = dict()

    if request.method == "POST":
        form = PropertyForm(request.POST)
        process_form = PropertyProcessForm(request.POST)
        if form.is_valid() and process_form.is_valid():
            instance = form.save(commit=False)

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            process_instance = process_form.save(commit=False)

            process_instance.property = instance
            process_instance.macro_status = PropertyProcess.AWAITINGVALUATION
            process_instance.furthest_status = PropertyProcess.AWAITINGVALUATION

            process_instance.created_by = request.user.get_full_name()
            process_instance.updated_by = request.user.get_full_name()

            process_instance.save()

            history_description = (
                f"{request.user.get_full_name()} has"
                " created the property process."
            )

            PropertyHistory.objects.create(
                propertyprocess=process_instance,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            data["propertyprocess_id"] = process_instance.id
        else:
            data["form_is_valid"] = False

    else:
        form = PropertyForm()
        process_form = PropertyProcessForm()

    context = {
        "form": form,
        "process_form": process_form,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_property_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_propertyprocess(request, property_id):
    """
    Ajax URL for adding a propertyprocess when property is already
    in the system
    """
    data = dict()

    if request.method == "POST":
        form = PropertyForm(request.POST)
        process_form = PropertyProcessForm(request.POST)
        property_instance = get_object_or_404(Property, id=property_id)
        if process_form.is_valid():
            instance = process_form.save(commit=False)

            instance.property = property_instance
            instance.macro_status = PropertyProcess.AWAITINGVALUATION
            instance.furthest_status = PropertyProcess.AWAITINGVALUATION

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            history_description = (
                f"{request.user.get_full_name()} has"
                " created the property process."
            )

            PropertyHistory.objects.create(
                propertyprocess=instance,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            data["propertyprocess_id"] = instance.id
        else:
            data["form_is_valid"] = False

    else:
        form = PropertyForm()
        process_form = PropertyProcessForm()

    context = {
        "form": form,
        "process_form": process_form,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_property_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def render_valuation(request, propertyprocess_id):
    """
    A view to return an ajax response with add valuation form
    """

    data = dict()

    employee = Profile.objects.get(user=request.user.id)
    instance = Valuation(valuer=employee)

    form = ValuationForm(instance=instance)
    marketing_form = SellerMarketingForm()

    context = {
        "form": form,
        "marketing_form": marketing_form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_valuation_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_valuation(request, propertyprocess_id):
    """
    Ajax URL for adding a valuation.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = ValuationForm(request.POST)
        marketing_form = SellerMarketingForm(request.POST)
        if form.is_valid() and marketing_form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            marketing_instance = marketing_form.save(commit=False)

            marketing_instance.propertyprocess = property_process

            marketing_instance.created_by = request.user.get_full_name()
            marketing_instance.updated_by = request.user.get_full_name()

            marketing_instance.save()

            property_process.macro_status = PropertyProcess.VALUATION
            property_process.furthest_status = PropertyProcess.VALUATION
            property_process.save()

            history_description = (
                f"{request.user.get_full_name()} has" " added a valuation."
            )

            history_description_two = (
                f"{request.user.get_full_name()} has" " added marketing info."
            )

            history_valuation = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description_two,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history_valuation": history_valuation,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        form = ValuationForm()
        marketing_form = SellerMarketingForm()

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "marketing_form": marketing_form,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_valuation_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def render_history_notes(request, history_id):
    """
    A view to return an ajax response with edit history notes form
    """

    data = dict()

    history_instance = get_object_or_404(PropertyHistory, id=history_id)

    form = HistoryNotesForm(instance=history_instance)

    context = {
        "form": form,
        "history_instance": history_instance,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/notes_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_history_notes(request, history_id):
    """
    A view to deal with form submission for history notes
    """
    data = dict()

    history_instance = get_object_or_404(PropertyHistory, id=history_id)

    if request.method == "POST":
        form = HistoryNotesForm(request.POST, instance=history_instance)
        if form.is_valid():
            instance = form.save(commit=False)

            if history_instance.notes == "":
                instance.created_by = request.user.get_full_name()

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        HistoryNotesForm(instance=history_instance)

    context = {
        "form": form,
        "history_instance": history_instance,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/notes_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def render_instruction(request, propertyprocess_id):
    """
    A view to return an ajax response with add instruction form
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    property = get_object_or_404(Property, id=property_process.property.id)

    form = InstructionForm()
    floor_space_form = FloorSpaceForm(instance=property)

    context = {
        "form": form,
        "floor_space_form": floor_space_form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_instruction_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_instruction(request, propertyprocess_id):
    """
    Ajax URL for adding a instruction.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    property = get_object_or_404(Property, id=property_process.property.id)

    if request.method == "POST":
        form = InstructionForm(request.POST)
        floor_space_form = FloorSpaceForm(request.POST, instance=property)
        if form.is_valid() and floor_space_form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            instance.send_mail(request)

            floor_space_form.save()

            property_process.macro_status = PropertyProcess.INSTRUCTION
            property_process.furthest_status = PropertyProcess.INSTRUCTION
            property_process.save()

            PropertyFees.objects.create(
                propertyprocess=property_process,
                fee=form.cleaned_data["fee_agreed"],
                price=form.cleaned_data["listing_price"],
                date=instance.date,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            history_description = (
                f"{request.user.get_full_name()} has added a instruction."
            )

            history_description_two = (
                f"{request.user.get_full_name()} has updated"
                " property info (floor space)."
            )

            history_valuation = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description_two,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history_valuation": history_valuation,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        form = InstructionForm()
        floor_space_form = FloorSpaceForm()

    context = {
        "form": form,
        "floor_space_form": floor_space_form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_instruction_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)
