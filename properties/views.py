import datetime
import humanize

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
    ReductionForm,
    OffererForm,
    OffererMortgageForm,
    OffererCashForm,
    OfferForm,
    AnotherOfferForm,
    OfferStatusForm,
    InstructionChangeForm,
    WithdrawalForm,
    DateForm,
    DealForm,
    BuyerMarketingForm,
    SoldMarketingBoardForm,
    PropertyFeesForm,
    ExchangeMoveForm,
)
from properties.models import (
    Property,
    PropertyProcess,
    PropertyFees,
    PropertyHistory,
    Instruction,
    InstructionChange,
    Offer,
    OffererDetails,
    OffererCash,
    PropertyChain,
    Valuation,
    OffererMortgage,
    Marketing,
    SalesProgression,
    SalesProgressionSettings,
    SalesProgressionPhase,
    Deal,
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
    offers = Offer.objects.filter(offerer_details=offerer_id)

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
            process_instance.furthest_status = (
                PropertyProcess.AWAITINGVALUATION
            )

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
                "history": history_valuation,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        employee = Profile.objects.get(user=request.user.id)
        instance = Valuation(valuer=employee)

        form = ValuationForm(instance=instance)
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

            history_instruction = PropertyHistory.objects.create(
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
                "history": history_instruction,
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


def add_reduction(request, propertyprocess_id):
    """
    Ajax URL for adding a reduction.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    property_fee = PropertyFees.objects.filter(
        propertyprocess=propertyprocess_id
    ).first()

    if request.method == "POST":
        form = ReductionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process
            instance.fee = abs(property_fee.fee)

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            history_description = (
                f"{request.user.get_full_name()} has added a reduction."
            )

            old_price = abs(property_fee.price)

            notes = (
                "The price has been reduced from "
                f"£{humanize.intcomma(old_price)}"
                f" to £{humanize.intcomma(instance.price)}"
            )

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        form = ReductionForm(
            initial={"date": datetime.date.today, "price": property_fee.price},
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_reduction_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_offerer(request, propertyprocess_id):
    """
    Ajax URL for adding a offerer.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = OffererForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
            if instance.funding == OffererDetails.MORTGAGE:
                data["url"] = reverse(
                    "properties:add_offerer_mortgage",
                    kwargs={
                        "propertyprocess_id": propertyprocess_id,
                        "offerer_id": instance.id,
                    },
                )
            else:
                data["url"] = reverse(
                    "properties:add_offerer_cash",
                    kwargs={
                        "propertyprocess_id": propertyprocess_id,
                        "offerer_id": instance.id,
                    },
                )
        else:
            data["form_is_valid"] = False

    else:
        form = OffererForm()

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_offerer_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_offerer_mortgage(request, propertyprocess_id, offerer_id):
    """
    Ajax URL for adding a offerer mortgage options.
    """
    data = dict()

    offerer = get_object_or_404(OffererDetails, id=offerer_id)

    if request.method == "POST":
        form = OffererMortgageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.offerer_details = offerer

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            if instance.verified_status == OffererMortgage.VERIFIEDMR:
                instance.verified = True
            elif instance.verified_status == OffererMortgage.MIP:
                instance.verified = True

            instance.save()

            data["form_is_valid"] = True

            data["url"] = reverse(
                "properties:add_offer",
                kwargs={
                    "propertyprocess_id": propertyprocess_id,
                    "offerer_id": offerer_id,
                },
            )
        else:
            data["form_is_valid"] = False

    else:
        form = OffererMortgageForm()

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "offerer_id": offerer_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_offerer_mortgage_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_offerer_cash(request, propertyprocess_id, offerer_id):
    """
    Ajax URL for adding a offerer cash options.
    """
    data = dict()

    offerer = get_object_or_404(OffererDetails, id=offerer_id)

    if request.method == "POST":
        form = OffererCashForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.offerer_details = offerer

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

            data["url"] = reverse(
                "properties:add_offer",
                kwargs={
                    "propertyprocess_id": propertyprocess_id,
                    "offerer_id": offerer_id,
                },
            )
        else:
            data["form_is_valid"] = False

    else:
        form = OffererCashForm()

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "offerer_id": offerer_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_offerer_cash_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_offer(request, propertyprocess_id, offerer_id):
    """
    Ajax URL for adding an offer.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    offerer = get_object_or_404(OffererDetails, id=offerer_id)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.offerer_details = offerer

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            history_description = (
                f"{request.user.get_full_name()} has added an offer."
            )

            notes = (
                f"A new offer has been added ({offerer.full_name}) "
                f"with funding marked as '{offerer.funding}'. "
                f"An initial offer of £{humanize.intcomma(instance.offer)}"
                " was added."
            )

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        form = OfferForm(initial={"date": datetime.date.today})

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "offerer": offerer,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_offer_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def add_another_offer(request, propertyprocess_id):
    """
    Ajax URL for adding an offer to an existing offerer.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = AnotherOfferForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            offerer_offers = Offer.objects.filter(
                offerer_details=instance.offerer_details.id
            )

            for offer in offerer_offers:
                if (
                    offer.status == Offer.GETTINGVERIFIED
                    or offer.status == Offer.NEGOTIATING
                ):
                    offer.status = Offer.REJECTED
                    offer.updated_by = request.user.get_full_name()
                offer.save()

            instance.save()

            offerer = get_object_or_404(
                OffererDetails, id=instance.offerer_details.id
            )

            history_description = (
                f"{request.user.get_full_name()} has added an offer."
            )

            notes = (
                f"An offer has been changed for ({offerer.full_name}). "
                f"The new offer is for £{humanize.intcomma(instance.offer)}"
            )

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        if "id" in request.GET:
            offerer_id = request.GET["id"]
            offerer = get_object_or_404(OffererDetails, id=offerer_id)
            form = AnotherOfferForm(
                initial={
                    "date": datetime.date.today,
                    "offerer_details": offerer,
                }
            )
        else:
            form = AnotherOfferForm(
                initial={
                    "date": datetime.date.today,
                }
            )

        form.fields[
            "offerer_details"
        ].queryset = OffererDetails.objects.filter(
            propertyprocess=propertyprocess_id
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_another_offer_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def edit_offerer_cash(request, offerer_id):
    """
    Ajax URL for editing an offerer's cash type.
    """

    data = dict()

    offerer = get_object_or_404(OffererDetails, id=offerer_id)
    property_process = get_object_or_404(
        PropertyProcess, id=offerer.propertyprocess.id
    )
    old_choice = offerer.offerer_cash_details.cash

    if request.method == "POST":
        form = OffererCashForm(
            request.POST, instance=offerer.offerer_cash_details
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has updated cash details."
            )

            for choice in OffererCash.CASH_CHOICES:
                if choice[0] == old_choice:
                    old_choice = choice[1]
                if choice[0] == instance.cash:
                    new_choice = choice[1]

            notes = (
                f"Cash option changed for ({offerer.full_name}). "
                f"Changing from '{old_choice}' to '{new_choice}'."
            )

            instance.save()

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        form = OffererCashForm(instance=offerer.offerer_cash_details)

    context = {
        "form": form,
        "offerer": offerer,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_offerer_cash_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def edit_offerer_mortgage(request, offerer_id):
    """
    Ajax URL for editing an offerer's mortgage type.
    """

    data = dict()

    offerer = get_object_or_404(OffererDetails, id=offerer_id)
    property_process = get_object_or_404(
        PropertyProcess, id=offerer.propertyprocess.id
    )
    old_deposit = offerer.offerer_mortgage_details.deposit_percentage
    old_verified = offerer.offerer_mortgage_details.verified_status

    if request.method == "POST":
        form = OffererMortgageForm(
            request.POST, instance=offerer.offerer_mortgage_details
        )
        if form.is_valid():
            instance = form.save(commit=False)

            if instance.verified_status == OffererMortgage.VERIFIEDMR:
                instance.verified = True
            elif instance.verified_status == OffererMortgage.MIP:
                instance.verified = True
            elif instance.verified_status == OffererMortgage.PENDING:
                instance.verified = False
            elif instance.verified_status == OffererMortgage.UNABLE:
                instance.verified = False

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has updated mortgage details."
            )

            for choice in OffererMortgage.VERI_CHOICES:
                if choice[0] == old_verified:
                    old_verified = choice[1]
                if choice[0] == instance.verified_status:
                    new_verified = choice[1]

            deposit_notes = ""
            if old_deposit != instance.deposit_percentage:
                deposit_notes = (
                    f"The deposit percentage has changed from {old_deposit}%"
                    f" to {round(instance.deposit_percentage, 2)}%. "
                )

            verified_notes = ""
            if old_verified != new_verified:
                verified_notes = (
                    f"The mortgage verification status has changed from {old_verified}"
                    f" to {new_verified}."
                )

            notes = deposit_notes + verified_notes

            instance.save()

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        form = OffererMortgageForm(instance=offerer.offerer_mortgage_details)

    context = {
        "form": form,
        "offerer": offerer,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_offerer_mortgage_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def edit_offer_status(request, offer_id):
    """
    Ajax URL for editing an offer status.
    """

    data = dict()

    offer = get_object_or_404(Offer, id=offer_id)
    property_process = get_object_or_404(
        PropertyProcess, id=offer.propertyprocess.id
    )
    old_status = offer.status

    if request.method == "POST":
        form = OfferStatusForm(request.POST, instance=offer)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has updated offer status."
            )

            for choice in Offer.STATUS:
                if choice[0] == old_status:
                    old_status = choice[1]
                if choice[0] == instance.status:
                    new_status = choice[1]

            notes = (
                f"The status for the offer from {offer.offerer_details.full_name}"
                f" for £{humanize.intcomma(instance.offer)} has been changed from "
                f"'{old_status}' to '{new_status}'."
            )

            instance.save()

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False

    else:
        form = OfferStatusForm(instance=offer)

    context = {
        "form": form,
        "offer": offer,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_offer_status_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def edit_instruction(request, propertyprocess_id):
    """
    Ajax URL for editing an instruction.
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )
    instruction = get_object_or_404(
        Instruction, propertyprocess=property_process.id
    )
    property_fee = PropertyFees.objects.filter(
        propertyprocess=property_process.id
    ).first()

    url = reverse(
        "properties:edit_instruction",
        kwargs={
            "propertyprocess_id": property_process.id,
        },
    )

    if request.method == "POST":
        form = InstructionChangeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            new_agreement_type = form.cleaned_data["agreement_type"]
            new_fee_agreed = form.cleaned_data["fee_agreed"]
            new_length_of_contract = int(
                form.cleaned_data["length_of_contract"]
            )

            instance.created_by = request.user.get_full_name()
            instance.propertyprocess = property_process

            for choice in Instruction.AGREEMENT_TYPE:
                if choice[0] == instruction.agreement_type:
                    old_agreement_type = choice[1]
                if choice[0] == new_agreement_type:
                    new_agreement_type = choice[1]

            for choice in Instruction.LENGTH_OF_CONTRACT:
                if choice[0] == instruction.length_of_contract:
                    old_length_of_contract = choice[1]
                if choice[0] == new_length_of_contract:
                    new_length_of_contract = choice[1]

            agreement_type_notes = ""
            if new_agreement_type != old_agreement_type:
                agreement_type_notes = (
                    "The instructed agreement type"
                    f" has changed from {old_agreement_type}"
                    f" to {new_agreement_type}. "
                )
                instance.agreement_type_bool = True

            fee_notes = ""
            if new_fee_agreed != instruction.fee_agreed:
                fee_notes = (
                    "The instructed fee has changed "
                    f"from {instruction.fee_agreed}%"
                    f" to {new_fee_agreed}%. "
                )
                instance.fee_agreed_bool = True
                PropertyFees.objects.create(
                    propertyprocess=property_process,
                    fee=new_fee_agreed,
                    price=property_fee.price,
                    date=datetime.date.today(),
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )

            length_of_contract_notes = ""
            if new_length_of_contract != old_length_of_contract:
                length_of_contract_notes = (
                    "The instructed length of contract "
                    f"has changed from {old_length_of_contract}"
                    f" to {new_length_of_contract}. "
                )
                instance.length_of_contract_bool = True

            instance.updated_by = request.user.get_full_name()

            instance.save()

            history_description = (
                f"{request.user.get_full_name()} has changed the Instruction."
            )

            notes = agreement_type_notes + fee_notes + length_of_contract_notes

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False
    else:
        agreement_type = instruction.agreement_type
        fee_agreed = instruction.fee_agreed
        length_of_contract = instruction.length_of_contract

        form = InstructionChangeForm(
            initial={
                "agreement_type": agreement_type,
                "fee_agreed": fee_agreed,
                "length_of_contract": length_of_contract,
            }
        )

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_instruction_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def edit_instruction_change(request, instruction_change_id):
    """
    Ajax URL for editing an instruction.
    """

    data = dict()

    instruction_change = get_object_or_404(
        InstructionChange, id=instruction_change_id
    )

    property_process = get_object_or_404(
        PropertyProcess, id=instruction_change.propertyprocess.id
    )

    property_fee = PropertyFees.objects.filter(
        propertyprocess=property_process.id
    ).first()

    url = reverse(
        "properties:edit_instruction_change",
        kwargs={
            "instruction_change_id": instruction_change.id,
        },
    )

    for choice in Instruction.AGREEMENT_TYPE:
        if choice[0] == instruction_change.agreement_type:
            old_agreement_type = choice[1]

    for choice in Instruction.LENGTH_OF_CONTRACT:
        if choice[0] == instruction_change.length_of_contract:
            old_length_of_contract = choice[1]

    old_fee = instruction_change.fee_agreed

    if request.method == "POST":
        form = InstructionChangeForm(request.POST, instance=instruction_change)
        if form.is_valid():
            instance = form.save(commit=False)

            new_agreement_type = form.cleaned_data["agreement_type"]
            new_fee_agreed = form.cleaned_data["fee_agreed"]
            new_length_of_contract = int(
                form.cleaned_data["length_of_contract"]
            )

            for choice in Instruction.AGREEMENT_TYPE:
                if choice[0] == new_agreement_type:
                    new_agreement_type = choice[1]

            for choice in Instruction.LENGTH_OF_CONTRACT:
                if choice[0] == new_length_of_contract:
                    new_length_of_contract = choice[1]

            agreement_type_notes = ""
            if new_agreement_type != old_agreement_type:
                agreement_type_notes = (
                    "The instructed agreement type"
                    f" has changed from {old_agreement_type}"
                    f" to {new_agreement_type}. "
                )
                instance.agreement_type_bool = True

            fee_notes = ""
            if new_fee_agreed != old_fee:
                fee_notes = (
                    "The instructed fee has changed "
                    f"from {old_fee}%"
                    f" to {new_fee_agreed}%. "
                )
                instance.fee_agreed_bool = True
                PropertyFees.objects.create(
                    propertyprocess=property_process,
                    fee=new_fee_agreed,
                    price=property_fee.price,
                    date=datetime.date.today(),
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )

            length_of_contract_notes = ""
            if new_length_of_contract != old_length_of_contract:
                length_of_contract_notes = (
                    "The instructed length of contract "
                    f"has changed from {old_length_of_contract}"
                    f" to {new_length_of_contract}. "
                )
                instance.length_of_contract_bool = True

            instance.updated_by = request.user.get_full_name()

            instance.save()

            history_description = (
                f"{request.user.get_full_name()} has changed the Instruction."
            )

            notes = agreement_type_notes + fee_notes + length_of_contract_notes

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True
            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )
        else:
            data["form_is_valid"] = False
    else:
        form = InstructionChangeForm(
            instance=instruction_change,
        )

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_instruction_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def withdraw_property(request, propertyprocess_id):
    """
    Ajax URL for withdrawing a property.
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data["withdrawal_reason"]
            date = form.cleaned_data["date"]

            if property_process.macro_status == PropertyProcess.DEAL:
                last_property_fee = PropertyFees.objects.filter(
                    propertyprocess=property_process
                ).first()
                minus_fee = last_property_fee.fee * -1
                PropertyFees.objects.create(
                    propertyprocess=property_process,
                    fee=minus_fee,
                    price=last_property_fee.price,
                    date=date,
                    active=True,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )
                Deal.objects.get(propertyprocess=property_process).delete()

            for offer_instance in property_process.offer.all():
                offer_instance.status = Offer.REJECTED
                offer_instance.save()

            property_process.macro_status = PropertyProcess.WITHDRAWN
            property_process.save()

            history_description = (
                f"{request.user.get_full_name()} has withdrawn this property."
            )

            for withdrawal_reason in WithdrawalForm.WITHDRAWN_REASON:
                if withdrawal_reason[0] == reason:
                    reason = withdrawal_reason[1]

            history_notes = reason

            for offer in property_process.offer.all():
                if (
                    offer.status == Offer.GETTINGVERIFIED
                    or offer.status == Offer.NEGOTIATING
                    or offer.status == Offer.ACCEPTED
                ):
                    offer.status = Offer.REJECTED

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=history_notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            property_process.send_withdrawn_mail(request, reason)

            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = WithdrawalForm(
            initial={"date": datetime.date.today},
        )
        context = {
            "property_process": property_process,
            "form": form,
        }
        data["html_modal"] = render_to_string(
            "properties/stages/withdraw_modal.html",
            context,
            request=request,
        )

    return JsonResponse(data)


def back_on_the_market(request, propertyprocess_id):
    """
    Ajax URL for putting a property back on the market.
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():

            property_process.macro_status = PropertyProcess.INSTRUCTION
            property_process.save()

            history_description = (
                f"{request.user.get_full_name()} has put the"
                " property back on the market."
            )

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            property_process.send_back_on_market_mail(request)

            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = DateForm(
            initial={"date": datetime.date.today},
        )
        context = {
            "property_process": property_process,
            "form": form,
        }
        data["html_modal"] = render_to_string(
            "properties/stages/back_on_the_market_modal.html",
            context,
            request=request,
        )

    return JsonResponse(data)


def add_deal(request, propertyprocess_id):
    """
    Ajax URL for adding a deal.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )
    marketing_instance = get_object_or_404(
        Marketing, propertyprocess=property_process
    )
    property_fee = PropertyFees.objects.filter(
        propertyprocess=property_process.id
    ).first()

    if request.method == "POST":
        form = DealForm(request.POST)
        marketing_form = BuyerMarketingForm(
            request.POST, instance=marketing_instance
        )
        marketing_board_form = SoldMarketingBoardForm(request.POST)
        if (
            form.is_valid()
            and marketing_form.is_valid()
            and marketing_board_form.is_valid()
        ):
            marketing_form.save()
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            offer_accepted = form.cleaned_data["offer_accepted"]
            offer_accepted_date = form.cleaned_data["date"]
            target_move_date = form.cleaned_data["target_move_date"]

            instance.save()

            property_process.macro_status = PropertyProcess.DEAL
            property_process.furthest_status = PropertyProcess.DEAL
            property_process.save()

            offer = Offer.objects.get(pk=offer_accepted.pk)

            for offer_instance in property_process.offer.all():
                if (
                    offer_instance.status == Offer.GETTINGVERIFIED
                    or offer_instance.status == Offer.NEGOTIATING
                    or offer_instance.status == Offer.ACCEPTED
                ):
                    if offer_instance.pk != offer.pk:
                        offer_instance.status = Offer.REJECTED
                        offer_instance.save()
                    if offer_instance.pk == offer.pk:
                        offer_instance.status = Offer.ACCEPTED
                        offer_instance.save()

            PropertyFees.objects.create(
                propertyprocess=property_process,
                fee=abs(property_fee.fee),
                price=offer.offer,
                date=offer_accepted_date,
                active=True,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            if not SalesProgression.objects.filter(
                propertyprocess=property_process
            ).exists():
                sales_prog = SalesProgression.objects.create(
                    propertyprocess=property_process,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )
                SalesProgressionSettings.objects.create(
                    sales_progression=sales_prog,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )
                SalesProgressionPhase.objects.create(
                    sales_progression=sales_prog,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )

            history_description = (
                f"{request.user.get_full_name()} has added a deal."
            )

            formatted_date = target_move_date.strftime("%d/%m/%Y")

            notes = (
                f"A deal been added ({offer.offerer_details.full_name}) "
                f"for £{humanize.intcomma(offer.offer)}. "
                f"The targeted move date is {formatted_date}."
            )

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            marketing_board = marketing_board_form.cleaned_data[
                "sold_marketing_board"
            ]

            if marketing_board == "True":
                marketing_board = True
            else:
                marketing_board = False

            instance.send_deal_mail(request, marketing_board)

            data["form_is_valid"] = True

            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )

        else:
            data["form_is_valid"] = False
    else:
        form = DealForm(initial={"date": datetime.date.today})
        marketing_form = BuyerMarketingForm(instance=marketing_instance)
        marketing_board_form = SoldMarketingBoardForm(
            initial={
                "sold_marketing_board": property_process.instruction.marketing_board
            }
        )

        form.fields["offer_accepted"].queryset = (
            Offer.objects.filter(propertyprocess=propertyprocess_id)
            .exclude(status=Offer.REJECTED)
            .exclude(status=Offer.WITHDRAWN)
        )

    context = {
        "form": form,
        "marketing_form": marketing_form,
        "marketing_board_form": marketing_board_form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_deal_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


def edit_deal(request, propertyprocess_id):
    """
    Ajax URL for editing a deal.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )
    property_fee = PropertyFees.objects.filter(
        propertyprocess=property_process.id
    ).first()

    if request.method == "POST":
        form = PropertyFeesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            new_fee = form.cleaned_data["fee"]
            new_price = form.cleaned_data["price"]

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.date = datetime.date.today()
            instance.active = True

            instance.save()

            property_fee.active = False

            property_fee.save()

            history_description = (
                f"{request.user.get_full_name()} has changed a deal."
            )

            fee_notes = ""
            if property_fee.fee != new_fee:
                fee_notes = (
                    f"The fee has been changed from {property_fee.fee}%"
                    f" to {new_fee}%. "
                )

            price_notes = ""
            if property_fee.price != new_price:
                price_notes = (
                    "The price has been changed from £"
                    f"{humanize.intcomma(property_fee.price)}"
                    f" to £{humanize.intcomma(new_price)}."
                )

            notes = fee_notes + price_notes

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True

            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )

        else:
            data["form_is_valid"] = False
    else:
        form = PropertyFeesForm(
            initial={
                "price": property_fee.price,
                "fee": property_fee.fee,
            }
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_deal_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


def add_exchange(request, propertyprocess_id):
    """
    Ajax URL for adding an exchange.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )
    property_fee = PropertyFees.objects.filter(
        propertyprocess=property_process.id
    ).first()

    if request.method == "POST":
        form = ExchangeMoveForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            exchange_date = form.cleaned_data["exchange_date"]
            completion_date = form.cleaned_data["completion_date"]

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            instance.send_exchange_mail(request)

            property_process.macro_status = PropertyProcess.COMPLETE
            property_process.save()

            history_description = (
                f"{request.user.get_full_name()} has added an exchange."
            )

            formatted_exchange_date = exchange_date.strftime("%d/%m/%Y")
            formatted_completion_date = completion_date.strftime("%d/%m/%Y")

            notes = (
                "An exchange/completion has been processed "
                f" with an exchange date of {formatted_exchange_date} "
                f"and a completion date of {formatted_completion_date}."
            )

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROPERTY_EVENT,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            data["form_is_valid"] = True

            context = {
                "property_process": property_process,
                "history": history,
            }
            data["html_success"] = render_to_string(
                "properties/stages/includes/form_success.html",
                context,
                request=request,
            )

        else:
            data["form_is_valid"] = False
    else:
        form = ExchangeMoveForm(
            initial={
                "exchange_date": datetime.date.today,
                "completion_date": datetime.date.today
            }
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_exchange_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)
