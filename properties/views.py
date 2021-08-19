import datetime
import humanize

from django_otp.decorators import otp_required

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string

from common.functions import (
    sales_progression_percentage,
    lettings_progression_percentage,
)
from lettings.models import LettingProperties
from properties.forms import (
    PropertyForm,
    PropertyProcessForm,
    ValuationForm,
    InstructionForm,
    InstructionLettingsExtraForm,
    SellerMarketingForm,
    HistoryNotesForm,
    FloorSpaceForm,
    ReductionForm,
    OffererForm,
    OffererMortgageForm,
    OffererCashForm,
    OffererLettingsForm,
    OfferForm,
    OfferLettingsForm,
    OfferLettingsExtraForm,
    AnotherOfferForm,
    AnotherOfferLettingsForm,
    OfferStatusForm,
    OfferStatusLettingsForm,
    OfferFormForm,
    InstructionChangeForm,
    WithdrawalForm,
    DateForm,
    DealForm,
    DealExtraForm,
    BuyerMarketingForm,
    SoldMarketingBoardForm,
    PropertyFeesForm,
    ExchangeMoveSalesForm,
    ExchangeMoveLettingsForm,
    SalesProgressionSettingsForm,
    SalesProgressionPhaseOneForm,
    SalesProgressionPhaseTwoForm,
    SalesProgressionPhaseThreeForm,
    SalesProgressionPhaseFourForm,
    PropertySellingInformationForm,
    ProgressionNotesForm,
    PropertyChainForm,
    SalesProgressionResetForm,
    LettingsProgressionSettingsForm,
    LettingsProgressionPhaseOneForm,
    LettingsProgressionPhaseTwoForm,
    LettingsProgressionPhaseThreeForm,
    LettingsProgressionPhaseFourForm,
)
from properties.models import (
    Property,
    PropertyProcess,
    PropertyFees,
    PropertyHistory,
    Instruction,
    InstructionLettingsExtra,
    InstructionChange,
    Offer,
    OffererDetails,
    OffererDetailsLettings,
    OffererCash,
    PropertyChain,
    Valuation,
    OffererMortgage,
    OfferLettingsExtra,
    Marketing,
    SalesProgression,
    SalesProgressionSettings,
    SalesProgressionPhase,
    Deal,
    ExchangeMove,
    DealExtraLettings,
    ProgressionNotes,
    PropertySellingInformation,
    LettingsProgression,
    LettingsProgressionSettings,
    LettingsProgressionPhase,
    Reduction,
)
from users.models import Profile


@otp_required
@login_required
def property_list(request):
    """
    A view to show paginated lists of the properties in the system; including
    searching and filtering.
    """

    properties_list = (
        PropertyProcess.objects
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
    archive = False

    if request.GET:
        if "archive" in request.GET:
            archive = request.GET["archive"]
            if archive == "true":
                archive = True
        if "status" in request.GET:
            status = request.GET["status"]
            if status == "potential":
                properties_list = (
                    properties_list.exclude(macro_status=3)
                    .exclude(macro_status=4)
                    .exclude(macro_status=5)
                )
            elif status == "live":
                properties_list = (
                    properties_list.exclude(macro_status=0)
                    .exclude(macro_status=1)
                    .exclude(macro_status=2)
                    .exclude(macro_status=4)
                    .exclude(macro_status=5)
                )
            elif status == "deal":
                properties_list = (
                    properties_list.exclude(macro_status=0)
                    .exclude(macro_status=1)
                    .exclude(macro_status=2)
                    .exclude(macro_status=3)
                    .exclude(macro_status=5)
                )
            elif status == "complete":
                properties_list = (
                    properties_list.exclude(macro_status=0)
                    .exclude(macro_status=1)
                    .exclude(macro_status=2)
                    .exclude(macro_status=3)
                    .exclude(macro_status=4)
                )
        if "sector" in request.GET:
            sector = request.GET["sector"]
            properties_list = properties_list.filter(sector=sector)
        if "query" in request.GET:
            query = request.GET["query"]
            if not query:
                return redirect(reverse("properties:property_list"))

            queries = (
                Q(property__postcode__icontains=query)
                | Q(property__address_line_1__icontains=query)
                | Q(property__address_line_2__icontains=query)
            )
            properties_list = properties_list.filter(queries)

    if archive is False:
        properties_list = (
            properties_list.exclude(macro_status=-1)
        )

    properties_list_length = len(properties_list)

    page = request.GET.get("page", 1)

    paginator = Paginator(properties_list, 16)
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
        "filter": filter,
        "archive": archive,
    }

    template = "properties/property_list.html"

    return render(request, template, context)


@otp_required
@login_required
def property_detail(request, propertyprocess_id):
    """
    A view to show individual property details
    """

    percentages = None
    property_chain = None

    propertyprocess = get_object_or_404(PropertyProcess, id=propertyprocess_id)
    property_history = propertyprocess.history.all()
    notes = propertyprocess.progression_notes.all()

    if propertyprocess.sector == PropertyProcess.SALES:
        offers = propertyprocess.offerer_details.all()
    else:
        offers = propertyprocess.offerer_details_lettings.all()

    if (
        propertyprocess.furthest_status > 3
        and propertyprocess.sector == PropertyProcess.SALES
    ):
        percentages = sales_progression_percentage(propertyprocess.id)
        property_chain = propertyprocess.property_chain.all()
    elif (
        propertyprocess.furthest_status > 3
        and propertyprocess.sector == PropertyProcess.LETTINGS
    ):
        percentages = lettings_progression_percentage(propertyprocess.id)

    property_history_list_length = len(property_history)
    offers_length = len(offers)
    notes_length = len(notes)

    history_page = 1
    offer_page = 1
    notes_page = 1

    history_paginator = Paginator(property_history, 4)
    offers_paginator = Paginator(offers, 4)
    notes_paginator = Paginator(notes, 5)

    history_last_page = history_paginator.num_pages
    offers_last_page = offers_paginator.num_pages
    notes_last_page = notes_paginator.num_pages

    try:
        property_history = history_paginator.page(history_page)
        offers = offers_paginator.page(offer_page)
        notes = notes_paginator.page(notes_page)
    except PageNotAnInteger:
        property_history = history_paginator.page(1)
        offers = offers_paginator.page(1)
        notes = notes_paginator.page(1)
    except EmptyPage:
        property_history = history_paginator.page(history_paginator.num_pages)
        offers = offers_paginator.page(offers_paginator.num_pages)
        notes = notes_paginator.page(notes_paginator.num_pages)

    context = {
        "propertyprocess": propertyprocess,
        "property_history": property_history,
        "property_history_length": property_history_list_length,
        "history_last_page": history_last_page,
        "offers": offers,
        "offers_length": offers_length,
        "offers_last_page": offers_last_page,
        "notes": notes,
        "notes_length": notes_length,
        "notes_last_page": notes_last_page,
        "percentages": percentages,
        "property_chain": property_chain,
    }

    template = "properties/property_detail.html"

    return render(request, template, context)


@otp_required
@login_required
def property_history_pagination(request, propertyprocess_id):
    """
    A view to return an ajax response with property history instance
    """

    data = dict()
    propertyprocess = get_object_or_404(PropertyProcess, id=propertyprocess_id)
    property_history = propertyprocess.history.all()

    property_history_list_length = len(property_history)

    history_page = request.GET.get("page", 1)

    history_paginator = Paginator(property_history, 4)
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


@otp_required
@login_required
def offers_pagination(request, propertyprocess_id):
    """
    A view to return an ajax response with offers instance
    """
    data = dict()

    propertyprocess = get_object_or_404(PropertyProcess, id=propertyprocess_id)

    if propertyprocess.sector == PropertyProcess.SALES:
        offers = propertyprocess.offerer_details.all()
    else:
        offers = propertyprocess.offerer_details_lettings.all()

    offers_length = len(offers)

    offer_page = request.GET.get("page", 1)

    offers_paginator = Paginator(offers, 4)

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

    if propertyprocess.sector == PropertyProcess.SALES:
        data["html_table"] = render_to_string(
            "properties/includes/detail_tabs/offer_table.html",
            context,
            request=request,
        )
    else:
        data["html_table"] = render_to_string(
            "properties/includes/detail_tabs/offer_lettings_table.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@otp_required
@login_required
def notes_pagination(request, propertyprocess_id):
    """
    A view to return an ajax response with notes instance
    """
    data = dict()

    propertyprocess = get_object_or_404(PropertyProcess, id=propertyprocess_id)
    notes = propertyprocess.progression_notes.all()

    notes_length = len(notes)

    notes_page = request.GET.get("page", 1)

    notes_paginator = Paginator(notes, 5)

    notes_last_page = notes_paginator.num_pages

    try:
        notes = notes_paginator.page(notes_page)
    except PageNotAnInteger:
        notes = notes_paginator.page(1)
    except EmptyPage:
        notes = notes_paginator.page(notes_paginator.num_pages)

    context = {
        "propertyprocess": propertyprocess,
        "notes": notes,
        "notes_length": notes_length,
        "notes_last_page": notes_last_page,
    }

    data["pagination"] = render_to_string(
        "properties/includes/detail/notes_pagination.html",
        context,
        request=request,
    )
    data["html_table"] = render_to_string(
        "properties/includes/detail/notes.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
def offer_history_lettings(request, offerer_id):
    """
    A view to return an ajax response with offerer offer history for lettings
    """

    data = dict()

    offerer = get_object_or_404(OffererDetailsLettings, pk=offerer_id)
    offers = Offer.objects.filter(offerer_lettings_details=offerer_id)

    context = {"offers": offers, "offerer": offerer}

    data["html_modal"] = render_to_string(
        "properties/includes/detail_tabs/offer_lettings_history.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
def add_property_chain_detail(request, propertyprocess_id):
    """
    A view to add a property chain instance
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    url = reverse(
        "properties:add_property_chain_detail",
        kwargs={
            "propertyprocess_id": propertyprocess_id,
        },
    )

    if request.method == "POST":
        form = PropertyChainForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = PropertyChainForm()

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/property_chain_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def edit_property_chain_detail(request, property_chain_id):
    """
    A view to add a property chain instance
    """

    data = dict()

    chain_instance = get_object_or_404(PropertyChain, id=property_chain_id)

    url = reverse(
        "properties:edit_property_chain_detail",
        kwargs={
            "property_chain_id": property_chain_id,
        },
    )

    if request.method == "POST":
        form = PropertyChainForm(request.POST, instance=chain_instance)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = PropertyChainForm(instance=chain_instance)

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/property_chain_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def delete_property_chain_detail(request, property_chain_id):
    """
    A view to add a property chain instance
    """

    data = dict()

    chain_instance = get_object_or_404(PropertyChain, id=property_chain_id)

    if request.method == "POST":
        chain_instance.delete()
        data["form_is_valid"] = True

    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
def add_lettings_instruction(request, propertyprocess_id):
    """
    Ajax URL for adding a instruction on a lettings property.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    property = get_object_or_404(Property, id=property_process.property.id)

    if request.method == "POST":
        form = InstructionForm(request.POST)
        instruction_lettings_extra_form = InstructionLettingsExtraForm(
            request.POST
        )
        floor_space_form = FloorSpaceForm(request.POST, instance=property)
        if (
            form.is_valid()
            and floor_space_form.is_valid()
            and instruction_lettings_extra_form.is_valid()
        ):
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            instance.send_mail(request)

            floor_space_form.save()

            lettings_extra_instance = instruction_lettings_extra_form.save(
                commit=False
            )

            service_level = instruction_lettings_extra_form.cleaned_data[
                "lettings_service_level"
            ]

            lettings_extra_instance.propertyprocess = property_process
            if service_level != InstructionLettingsExtra.INTRO:
                lettings_extra_instance.managed_property = True

            lettings_extra_instance.created_by = request.user.get_full_name()
            lettings_extra_instance.updated_by = request.user.get_full_name()

            lettings_extra_instance.save()

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
        instruction_lettings_extra_form = InstructionLettingsExtraForm()
        floor_space_form = FloorSpaceForm()

    context = {
        "form": form,
        "instruction_lettings_extra_form": instruction_lettings_extra_form,
        "floor_space_form": floor_space_form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_instruction_lettings_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
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

            date = form.cleaned_data["date"]
            new_price = form.cleaned_data["price"]

            instance.save()

            Reduction.objects.create(
                propertyprocess=property_process,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
                date=date,
                price_change=new_price,
            )

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


@otp_required
@login_required
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


@otp_required
@login_required
def add_offer_form(request, propertyprocess_id, offerer_id):
    """
    Ajax URL for updating offer form status.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    offerer = get_object_or_404(OffererDetails, id=offerer_id)

    if request.method == "POST":
        form = OfferFormForm(
            request.POST,
            instance=offerer,
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            history_description = (
                f"{request.user.get_full_name()} has updated an offer form."
            )

            notes = (
                f"The offer form for {offerer.full_name} " "has been updated."
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

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        form = OfferFormForm(instance=offerer)

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "offerer_id": offerer_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_offer_form_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
def add_offerer_lettings(request, propertyprocess_id):
    """
    Ajax URL for adding a offerer for lettings properties.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = OffererLettingsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
            data["url"] = reverse(
                "properties:add_offer_lettings",
                kwargs={
                    "propertyprocess_id": propertyprocess_id,
                    "offerer_id": instance.id,
                },
            )
        else:
            data["form_is_valid"] = False

    else:
        form = OffererLettingsForm()
        form_lettings = OfferLettingsExtraForm()

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_offerer_lettings_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
def add_offer_lettings(request, propertyprocess_id, offerer_id):
    """
    Ajax URL for adding an offer.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    offerer = get_object_or_404(OffererDetailsLettings, id=offerer_id)

    if request.method == "POST":
        form = OfferLettingsForm(request.POST)
        form_lettings = OfferLettingsExtraForm(request.POST)
        if form.is_valid() and form_lettings.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.offerer_lettings_details = offerer

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance_lettings = form_lettings.save(commit=False)

            instance_lettings.offer_extra = instance

            instance.save()

            instance_lettings.created_by = request.user.get_full_name()
            instance_lettings.updated_by = request.user.get_full_name()

            instance_lettings.save()

            history_description = (
                f"{request.user.get_full_name()} has added an offer."
            )

            notes = (
                f"A new offer has been added ({offerer.full_name}). "
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
        form = OfferLettingsForm(initial={"date": datetime.date.today})
        form_lettings = OfferLettingsExtraForm()

    context = {
        "form": form,
        "form_lettings": form_lettings,
        "propertyprocess_id": propertyprocess_id,
        "offerer": offerer,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_offer_lettings_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
def add_another_lettings_offer(request, propertyprocess_id):
    """
    Ajax URL for adding an offer to an existing offerer (lettings).
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = AnotherOfferLettingsForm(request.POST)
        form_lettings = OfferLettingsExtraForm(request.POST)
        if form.is_valid() and form_lettings.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            offerer_offers = Offer.objects.filter(
                offerer_lettings_details=instance.offerer_lettings_details.id
            )

            for offer in offerer_offers:
                if (
                    offer.status == Offer.GETTINGVERIFIED
                    or offer.status == Offer.NEGOTIATING
                ):
                    offer.status = Offer.REJECTED
                    offer.updated_by = request.user.get_full_name()
                offer.save()

            instance_lettings = form_lettings.save(commit=False)

            instance_lettings.offer_extra = instance

            instance.save()

            instance_lettings.created_by = request.user.get_full_name()
            instance_lettings.updated_by = request.user.get_full_name()

            instance_lettings.save()

            offerer = get_object_or_404(
                OffererDetailsLettings, id=instance.offerer_lettings_details.id
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
            offerer = get_object_or_404(OffererDetailsLettings, id=offerer_id)
            form = AnotherOfferLettingsForm(
                initial={
                    "date": datetime.date.today,
                    "offerer_lettings_details": offerer,
                }
            )
            exists = False
            try:
                exists = (
                    offerer.offerdetailslettings.first().offer_extra
                    is not None
                )
            except OfferLettingsExtra.DoesNotExist:
                pass

            if exists:
                form_lettings = OfferLettingsExtraForm(
                    initial={
                        "proposed_move_in_date": offerer.offerdetailslettings.first().offer_extra.proposed_move_in_date,
                        "term": offerer.offerdetailslettings.first().offer_extra.term,
                    }
                )
            else:
                form_lettings = OfferLettingsExtraForm()
        else:
            form = AnotherOfferLettingsForm(
                initial={
                    "date": datetime.date.today,
                }
            )
            form_lettings = OfferLettingsExtraForm()

        form.fields[
            "offerer_lettings_details"
        ].queryset = OffererDetailsLettings.objects.filter(
            propertyprocess=propertyprocess_id
        )

    context = {
        "form": form,
        "form_lettings": form_lettings,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_another_lettings_offer_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
def edit_offer_lettings_status(request, offer_id):
    """
    Ajax URL for editing an offer status, lettings.
    """

    data = dict()

    offer = get_object_or_404(Offer, id=offer_id)
    property_process = get_object_or_404(
        PropertyProcess, id=offer.propertyprocess.id
    )
    old_status = offer.status

    if request.method == "POST":
        form = OfferStatusLettingsForm(request.POST, instance=offer)
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
                f"The status for the offer from {offer.offerer_lettings_details.full_name}"
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
        form = OfferStatusLettingsForm(instance=offer)

    context = {
        "form": form,
        "offer": offer,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/edit_offer_status_lettings_modal.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
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
                if property_process.sector == PropertyProcess.SALES:
                    Deal.objects.get(propertyprocess=property_process).delete()
                else:
                    DealExtraLettings.objects.get(
                        deal=property_process.deal
                    ).delete()
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

            formatted_date = date.strftime("%d/%m/%Y")

            full_note = reason + f" - Withdrawn on {formatted_date}"

            history_notes = full_note

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


@otp_required
@login_required
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


@otp_required
@login_required
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


@otp_required
@login_required
def add_deal_lettings(request, propertyprocess_id):
    """
    Ajax URL for adding a deal for lettings.
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
        deal_extra_form = DealExtraForm(request.POST)
        marketing_form = BuyerMarketingForm(
            request.POST, instance=marketing_instance
        )
        marketing_board_form = SoldMarketingBoardForm(request.POST)
        if (
            form.is_valid()
            and deal_extra_form.is_valid()
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

            deal_extra_instance = deal_extra_form.save(commit=False)

            deal_extra_instance.deal = instance

            deal_extra_instance.created_by = request.user.get_full_name()
            deal_extra_instance.updated_by = request.user.get_full_name()

            instance.save()

            deal_extra_instance.save()

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

            if not LettingsProgression.objects.filter(
                propertyprocess=property_process
            ).exists():
                lettings_prog = LettingsProgression.objects.create(
                    propertyprocess=property_process,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )
                LettingsProgressionSettings.objects.create(
                    lettings_progression=lettings_prog,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )
                LettingsProgressionPhase.objects.create(
                    lettings_progression=lettings_prog,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )

            history_description = (
                f"{request.user.get_full_name()} has added a deal."
            )

            formatted_date = target_move_date.strftime("%d/%m/%Y")

            notes = (
                f"A deal been added ({offer.offerer_lettings_details.full_name}"
                f") for £{humanize.intcomma(offer.offer)}. "
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

            instance.send_lettings_deal_mail(request, marketing_board)

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
        deal_extra_form = DealExtraForm()
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
        "deal_extra_form": deal_extra_form,
        "marketing_form": marketing_form,
        "marketing_board_form": marketing_board_form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_deal_lettings_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
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


@otp_required
@login_required
def add_exchange(request, propertyprocess_id):
    """
    Ajax URL for adding an exchange.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = ExchangeMoveSalesForm(request.POST)
        if form.is_valid():
            exchange_instance = ExchangeMove.objects.create(
                propertyprocess=property_process,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            instance = form.save(commit=False)

            exchange_date = form.cleaned_data["exchange_date"]
            completion_date = form.cleaned_data["completion_date"]

            instance.exchange = exchange_instance

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            instance.send_exchange_mail(request)

            property_process.macro_status = PropertyProcess.COMPLETE
            property_process.furthest_status = PropertyProcess.COMPLETE
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
        form = ExchangeMoveSalesForm(
            initial={
                "exchange_date": datetime.date.today,
                "completion_date": datetime.date.today,
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


@otp_required
@login_required
def add_exchange_lettings(request, propertyprocess_id):
    """
    Ajax URL for adding a lettings exchange.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = ExchangeMoveLettingsForm(request.POST)
        if form.is_valid():
            exchange_instance = ExchangeMove.objects.create(
                propertyprocess=property_process,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            instance = form.save(commit=False)

            move_in_date = form.cleaned_data["move_in_date"]
            first_renewal = form.cleaned_data["first_renewal"]

            instance.exchange = exchange_instance

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            LettingProperties.objects.create(
                propertyprocess=property_process,
                lettings_service_level=property_process.instruction_letting_extra.lettings_service_level,
                is_active=True,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

            instance.send_exchange_mail(request)

            property_process.macro_status = PropertyProcess.COMPLETE
            property_process.furthest_status = PropertyProcess.COMPLETE
            property_process.save()

            history_description = f"{request.user.get_full_name()} has added a lettings exchange."

            formatted_move_in_date = move_in_date.strftime("%d/%m/%Y")
            formatted_first_renewal = first_renewal.strftime("%d/%m/%Y")

            notes = (
                "An lettings completion has been processed "
                f" with an move in date of {formatted_move_in_date} "
                f"and a first renewal date of "
                f"{formatted_first_renewal}."
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
        form = ExchangeMoveLettingsForm(
            initial={
                "move_in_date": datetime.date.today,
            }
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/stages/add_exchange_lettings_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def edit_sales_prog_settings(request, propertyprocess_id):
    """
    Ajax URL for editing sales progression settings.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = SalesProgressionSettingsForm(
            request.POST,
            instance=property_process.sales_progression.sales_progression_settings,
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = SalesProgressionSettingsForm(
            instance=property_process.sales_progression.sales_progression_settings
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/edit_sales_prog_settings_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def phase_one(request, propertyprocess_id):
    """
    Ajax URL for phase one sales progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    sales_prog_phase = get_object_or_404(
        SalesProgressionPhase,
        sales_progression=property_process.sales_progression.id,
    )

    progression = property_process.sales_progression

    old_aml = progression.buyers_aml_checks_and_sales_memo
    old_initial_sol = progression.buyers_initial_solicitors_paperwork
    old_sellers_initial_sol = progression.sellers_inital_solicitors_paperwork
    old_draft_contracts = (
        progression.draft_contracts_recieved_by_buyers_solicitors
    )
    old_searches_paid = progression.searches_paid_for
    old_searches_ordered = progression.searches_ordered

    if request.method == "POST":
        form = SalesProgressionPhaseOneForm(request.POST, instance=progression)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated sales progression."
            )

            notes_dict = []

            if old_aml != instance.buyers_aml_checks_and_sales_memo:
                aml_notes = "Buyers AML Checks & Sales Memo"
                notes_dict.append(aml_notes)
                instance.buyers_aml_checks_and_sales_memo_date = (
                    datetime.date.today()
                )

            if old_initial_sol != instance.buyers_initial_solicitors_paperwork:
                sol_notes = "Buyers Initial Paperwork"
                notes_dict.append(sol_notes)
                instance.buyers_initial_solicitors_paperwork_date = (
                    datetime.date.today()
                )

            if (
                old_sellers_initial_sol
                != instance.sellers_inital_solicitors_paperwork
            ):
                seller_sol_notes = "Sellers Initial Paperwork"
                notes_dict.append(seller_sol_notes)
                instance.sellers_inital_solicitors_paperwork_date = (
                    datetime.date.today()
                )

            if (
                old_draft_contracts
                != instance.draft_contracts_recieved_by_buyers_solicitors
            ):
                draft_contract_notes = (
                    "Draft Contracts Received By Buyers Solicitors"
                )
                notes_dict.append(draft_contract_notes)
                instance.draft_contracts_recieved_by_buyers_solicitors_date = (
                    datetime.date.today()
                )

            if old_searches_paid != instance.searches_paid_for:
                searches_paid_notes = "Searches Paid For"
                notes_dict.append(searches_paid_notes)
                instance.searches_paid_for_date = datetime.date.today()

            if old_searches_ordered != instance.searches_ordered:
                searches_ordered_notes = "Searches Ordered"
                notes_dict.append(searches_ordered_notes)
                instance.searches_ordered_date = datetime.date.today()

            instance.save()

            phases = sales_progression_percentage(property_process.id)

            phase_one = phases.get("phase_1")
            if phase_one == 100:
                sales_prog_phase.phase_1 = True
                sales_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = SalesProgressionPhaseOneForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/phase_one_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def phase_two(request, propertyprocess_id):
    """
    Ajax URL for phase two sales progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    sales_prog_phase = get_object_or_404(
        SalesProgressionPhase,
        sales_progression=property_process.sales_progression.id,
    )

    progression = property_process.sales_progression

    old_mor_submitted = progression.mortgage_application_submitted
    old_mor_survey = progression.mortgage_survey_arranged
    old_mor_offer = progression.mortgage_offer_with_solicitors
    old_search = progression.all_search_results_recieved

    if request.method == "POST":
        form = SalesProgressionPhaseTwoForm(request.POST, instance=progression)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated sales progression."
            )

            notes_dict = []

            if old_mor_submitted != instance.mortgage_application_submitted:
                mor_notes = "Mortgage Application Submitted"
                notes_dict.append(mor_notes)
                instance.mortgage_application_submitted_date = (
                    datetime.date.today()
                )

            if old_mor_survey != instance.mortgage_survey_arranged:
                mor_sur_notes = "Mortgage Survey Booked"
                notes_dict.append(mor_sur_notes)
                instance.mortgage_survey_arranged_date = datetime.date.today()

            if old_mor_offer != instance.mortgage_offer_with_solicitors:
                mor_offer_notes = "Mortgage Offer With Solicitors"
                notes_dict.append(mor_offer_notes)
                instance.mortgage_offer_with_solicitors_date = (
                    datetime.date.today()
                )

            if old_search != instance.all_search_results_recieved:
                search_notes = "All Search Results Received"
                notes_dict.append(search_notes)
                instance.all_search_results_recieved_date = (
                    datetime.date.today()
                )

            instance.save()

            phases = sales_progression_percentage(property_process.id)

            phase_two = phases.get("phase_2")
            if phase_two == 100:
                sales_prog_phase.phase_2 = True
                sales_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = SalesProgressionPhaseTwoForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "propertyprocess": property_process,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/phase_two_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def phase_three(request, propertyprocess_id):
    """
    Ajax URL for phase three sales progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    sales_prog_phase = get_object_or_404(
        SalesProgressionPhase,
        sales_progression=property_process.sales_progression.id,
    )

    progression = property_process.sales_progression

    old_enquries = progression.enquiries_raised
    old_enquries_answered = progression.enquiries_answered
    old_survey = progression.structural_survey_booked
    old_survey_comp = progression.structural_survey_completed

    if request.method == "POST":
        form = SalesProgressionPhaseThreeForm(
            request.POST, instance=progression
        )
        if form.is_valid():

            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated sales progression."
            )

            notes_dict = []

            if old_enquries != instance.enquiries_raised:
                enq_notes = "Enquiries Raised"
                notes_dict.append(enq_notes)
                instance.enquiries_raised_date = datetime.date.today()

            if old_enquries_answered != instance.enquiries_answered:
                enq_answered_notes = "Enquiries Answered"
                notes_dict.append(enq_answered_notes)
                instance.enquiries_answered_date = datetime.date.today()

            if old_survey != instance.structural_survey_booked:
                survey_notes = "Structural Survey Booked"
                notes_dict.append(survey_notes)
                instance.structural_survey_booked_date = datetime.date.today()

            if old_survey_comp != instance.structural_survey_completed:
                survey_complete_notes = "Structural Survey Complete"
                notes_dict.append(survey_complete_notes)
                instance.structural_survey_completed_date = (
                    datetime.date.today()
                )

            instance.save()

            phases = sales_progression_percentage(property_process.id)

            phase_three = phases.get("phase_3")
            if phase_three == 100:
                sales_prog_phase.phase_3 = True
                sales_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = SalesProgressionPhaseThreeForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "propertyprocess": property_process,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/phase_three_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def phase_four(request, propertyprocess_id):
    """
    Ajax URL for phase one sales progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    sales_prog_phase = get_object_or_404(
        SalesProgressionPhase,
        sales_progression=property_process.sales_progression.id,
    )

    progression = property_process.sales_progression

    old_add_enquiries = progression.additional_enquiries_raised
    old_equiries_answered = progression.all_enquiries_answered
    old_contracts_sent = progression.final_contracts_sent_out
    old_buyers_contracts = progression.buyers_final_contracts_signed
    old_sellers_contracts = progression.sellers_final_contracts_signed
    old_deposit = progression.buyers_deposit_sent
    old_deposit_received = progression.buyers_deposit_recieved
    old_comp_date = progression.completion_date_agreed

    if request.method == "POST":
        form = SalesProgressionPhaseFourForm(
            request.POST, instance=progression
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated sales progression."
            )

            notes_dict = []

            if old_add_enquiries != instance.additional_enquiries_raised:
                additional_enquiries_notes = "Additional Enquiries Raised"
                notes_dict.append(additional_enquiries_notes)
                instance.additional_enquiries_raised_date = (
                    datetime.date.today()
                )

            if old_equiries_answered != instance.all_enquiries_answered:
                enquiries_answered_notes = "All Enquiries Answered"
                notes_dict.append(enquiries_answered_notes)
                instance.all_enquiries_answered_date = datetime.date.today()

            if old_contracts_sent != instance.final_contracts_sent_out:
                contracts_sent_notes = "Final Contracts Sent Out"
                notes_dict.append(contracts_sent_notes)
                instance.final_contracts_sent_out_date = datetime.date.today()

            if old_buyers_contracts != instance.buyers_final_contracts_signed:
                buyers_contract_notes = "Buyers Final Contracts Signed"
                notes_dict.append(buyers_contract_notes)
                instance.buyers_final_contracts_signed_date = (
                    datetime.date.today()
                )

            if (
                old_sellers_contracts
                != instance.sellers_final_contracts_signed
            ):
                seller_contract_notes = "Sellers Final Contracts Signed"
                notes_dict.append(seller_contract_notes)
                instance.sellers_final_contracts_signed_date = (
                    datetime.date.today()
                )

            if old_deposit != instance.buyers_deposit_sent:
                deposit_notes = "Buyers Deposit Sent"
                notes_dict.append(deposit_notes)
                instance.buyers_deposit_sent_date = datetime.date.today()

            if old_deposit_received != instance.buyers_deposit_recieved:
                deposit_received_notes = "Buyers Deposit Received"
                notes_dict.append(deposit_received_notes)
                instance.buyers_deposit_recieved_date = datetime.date.today()

            if old_comp_date != instance.completion_date_agreed:
                comp_notes = "Completion Date Agreed"
                notes_dict.append(comp_notes)
                instance.completion_date_agreed_date = datetime.date.today()

            instance.save()

            phases = sales_progression_percentage(property_process.id)

            phase_four = phases.get("phase_4")
            if phase_four == 100:
                sales_prog_phase.phase_4 = True
                sales_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = SalesProgressionPhaseFourForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/phase_four_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def add_client_info(request, propertyprocess_id):
    """
    Ajax URL for adding client info
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    url = reverse(
        "properties:add_client_info",
        kwargs={
            "propertyprocess_id": propertyprocess_id,
        },
    )

    if request.method == "POST":
        form = PropertySellingInformationForm(
            request.POST,
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = PropertySellingInformationForm()

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/client_info_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def edit_client_info(request, propertyprocess_id):
    """
    Ajax URL for editing client info
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    url = reverse(
        "properties:edit_client_info",
        kwargs={
            "propertyprocess_id": propertyprocess_id,
        },
    )

    if request.method == "POST":
        form = PropertySellingInformationForm(
            request.POST, instance=property_process.selling_information
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = PropertySellingInformationForm(
            instance=property_process.selling_information
        )

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/client_info_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def edit_progression_notes(request, progression_notes_id):
    """
    Ajax URL for editing progression notes
    """
    data = dict()

    progression = get_object_or_404(ProgressionNotes, id=progression_notes_id)

    url = reverse(
        "properties:edit_progression_notes",
        kwargs={
            "progression_notes_id": progression_notes_id,
        },
    )

    if request.method == "POST":
        form = ProgressionNotesForm(request.POST, instance=progression)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = ProgressionNotesForm(instance=progression)

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/progression_notes_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def add_progression_notes(request, propertyprocess_id):
    """
    Ajax URL for adding progression notes
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    url = reverse(
        "properties:add_progression_notes",
        kwargs={
            "propertyprocess_id": propertyprocess_id,
        },
    )

    if request.method == "POST":
        form = ProgressionNotesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.propertyprocess = property_process

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = ProgressionNotesForm()

    context = {
        "form": form,
        "url": url,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/progression_notes_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def delete_progression_notes(request, progression_notes_id):
    """
    Ajax URL for deleting progression notes
    """
    data = dict()

    progression = get_object_or_404(ProgressionNotes, id=progression_notes_id)

    if request.method == "POST":
        progression.delete()
        data["form_is_valid"] = True

    else:
        context = {
            "progression": progression,
        }
        data["html_modal"] = render_to_string(
            "properties/sales_progression/delete_progression_notes_modal.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@otp_required
@login_required
def fall_through(request, propertyprocess_id):
    """
    Ajax URL for editing a deal.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        property_process.previously_fallen_through = True
        property_process.macro_status = PropertyProcess.INSTRUCTION
        property_process.updated_by = request.user.get_full_name()
        property_process.save()

        deal_instance = Deal.objects.get(propertyprocess=property_process.id)

        offerer = deal_instance.offer_accepted.offerer_details.full_name

        offer_amount = deal_instance.offer_accepted.offer

        notes = (
            "The deal fallen through was with "
            f"{offerer} for £"
            f"{humanize.intcomma(offer_amount)}."
        )

        deal_instance.delete()

        property_fee_instance = PropertyFees.objects.filter(
            propertyprocess=property_process.id
        ).first()

        minus_fee = property_fee_instance.fee * -1

        PropertyFees.objects.create(
            propertyprocess=property_process,
            fee=minus_fee,
            price=property_fee_instance.price,
            date=datetime.date.today(),
            active=True,
            created_by=request.user.get_full_name(),
            updated_by=request.user.get_full_name(),
        )

        history_description = (
            f"{request.user.get_full_name()} has fallen through the property."
        )

        history = PropertyHistory.objects.create(
            propertyprocess=property_process,
            type=PropertyHistory.PROPERTY_EVENT,
            description=history_description,
            notes=notes,
            created_by=request.user.get_full_name(),
            updated_by=request.user.get_full_name(),
        )

        for offer_instance in property_process.offer.all():
            if (
                offer_instance.status == Offer.GETTINGVERIFIED
                or offer_instance.status == Offer.NEGOTIATING
                or offer_instance.status == Offer.ACCEPTED
            ):
                offer_instance.status = Offer.REJECTED
                offer_instance.save()

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
        context = {
            "property_process": property_process,
        }
        data["html_modal"] = render_to_string(
            "properties/sales_progression/fall_through_modal.html",
            context,
            request=request,
        )

    return JsonResponse(data)


@otp_required
@login_required
def manage_sales_progression(request, propertyprocess_id):
    """
    Ajax URL for editing sales progression after a fall through
    """

    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = SalesProgressionResetForm(request.POST)
        if form.is_valid():
            client_info = form.cleaned_data["client_info"]
            sales_progression = form.cleaned_data["sales_progression"]
            property_chain = form.cleaned_data["property_chain"]
            property_notes = form.cleaned_data["property_notes"]

            notes_dict = []

            if client_info:
                try:
                    client_info_instance = (
                        PropertySellingInformation.objects.get(
                            propertyprocess=property_process
                        )
                    )
                except PropertySellingInformation.DoesNotExist:
                    client_info_instance = None

                if client_info_instance:
                    client_info_instance.delete()

                client_info_notes = "Solicitor/Broker/Client Information"
                notes_dict.append(client_info_notes)

            if property_chain:
                property_chain_qs = PropertyChain.objects.filter(
                    propertyprocess=property_process
                )

                for property_chain_instance in property_chain_qs:
                    property_chain_instance.delete()

                property_chain_notes = "Property Chain"
                notes_dict.append(property_chain_notes)

            if property_notes:
                try:
                    progression_notes_instance = ProgressionNotes.objects.get(
                        propertyprocess=property_process
                    )
                except ProgressionNotes.DoesNotExist:
                    progression_notes_instance = None

                if progression_notes_instance:
                    progression_notes_instance.delete()

                progression_notes_notes = "Progression Notes"
                notes_dict.append(progression_notes_notes)

            if sales_progression:
                try:
                    sales_progression_instance = SalesProgression.objects.get(
                        propertyprocess=property_process
                    )
                except SalesProgression.DoesNotExist:
                    sales_progression_instance = None

                sales_progression_notes = "Sales Progression"
                notes_dict.append(sales_progression_notes)

                try:
                    sales_progression_settings_instance = (
                        SalesProgressionSettings.objects.get(
                            sales_progression=sales_progression_instance
                        )
                    )
                except SalesProgression.DoesNotExist:
                    sales_progression_settings_instance = None

                try:
                    sales_progression_phase_instance = (
                        SalesProgressionPhase.objects.get(
                            sales_progression=sales_progression_instance
                        )
                    )
                except SalesProgression.DoesNotExist:
                    sales_progression_phase_instance = None

                if sales_progression_settings_instance:
                    sales_progression_settings_instance.delete()
                if sales_progression_phase_instance:
                    sales_progression_phase_instance.delete()
                if sales_progression_instance:
                    sales_progression_instance.delete()

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

                notes = "The following has been cleared, "

            history_description = (
                f"{request.user.get_full_name()} has cleared some data."
            )

            notes = "The following data has been cleared "

            if (
                client_info is False
                and sales_progression is False
                and property_chain is False
                and property_notes is False
            ):
                data["form_is_valid"] = False
            else:
                for i, note in enumerate(notes_dict):
                    if len(notes_dict) == 1:
                        notes += note
                        notes += "."
                    else:
                        if i == len(notes_dict) - 1:
                            notes += note
                            notes += "."
                        elif i == len(notes_dict) - 2:
                            notes += note
                            notes += " and "
                        else:
                            notes += note
                            notes += ", "

                history = PropertyHistory.objects.create(
                    propertyprocess=property_process,
                    type=PropertyHistory.PROGRESSION,
                    description=history_description,
                    notes=notes,
                    created_by=request.user.get_full_name(),
                    updated_by=request.user.get_full_name(),
                )

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
        form = SalesProgressionResetForm()

    context = {
        "form": form,
        "property_process": property_process,
    }
    data["html_modal"] = render_to_string(
        "properties/sales_progression/manage_sales_progression_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def edit_lettings_prog_settings(request, propertyprocess_id):
    """
    Ajax URL for editing lettings progression settings.
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    if request.method == "POST":
        form = LettingsProgressionSettingsForm(
            request.POST,
            instance=property_process.lettings_progression.lettings_progression_settings,
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True

        else:
            data["form_is_valid"] = False
    else:
        form = LettingsProgressionSettingsForm(
            instance=property_process.lettings_progression.lettings_progression_settings,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/lettings_progression/edit_lettings_prog_settings_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def lettings_phase_one(request, propertyprocess_id):
    """
    Ajax URL for phase one lettings progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    lettings_prog_phase = get_object_or_404(
        LettingsProgressionPhase,
        lettings_progression=property_process.lettings_progression.id,
    )

    progression = property_process.lettings_progression

    old_touch_point = progression.contact_touch_point_to_ll_and_tt
    old_reference = progression.reference_forms_sent_to_tenant
    old_compliance = progression.compliance_form_sent_to_landlord
    old_google = progression.google_drive_and_email_inbox
    old_tenancy = progression.tenancy_created_on_expert_agent

    if request.method == "POST":
        form = LettingsProgressionPhaseOneForm(
            request.POST,
            instance=progression,
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated lettings progression."
            )

            notes_dict = []

            if old_touch_point != instance.contact_touch_point_to_ll_and_tt:
                old_touch_point_notes = "Contact Touch Point To LL & TT"
                notes_dict.append(old_touch_point_notes)
                instance.contact_touch_point_to_ll_and_tt_date = (
                    datetime.date.today()
                )

            if old_reference != instance.reference_forms_sent_to_tenant:
                old_reference_notes = "Referencing Forms Sent To Tenant"
                notes_dict.append(old_reference_notes)
                instance.reference_forms_sent_to_tenant_date = (
                    datetime.date.today()
                )

            if old_compliance != instance.compliance_form_sent_to_landlord:
                old_compliance_notes = "Compliance Form Sent To Landlord"
                notes_dict.append(old_compliance_notes)
                instance.compliance_form_sent_to_landlord_date = (
                    datetime.date.today()
                )

            if old_google != instance.google_drive_and_email_inbox:
                old_google_notes = "Google Drive & Email Inbox Created"
                notes_dict.append(old_google_notes)
                instance.google_drive_and_email_inbox_date = (
                    datetime.date.today()
                )

            if old_tenancy != instance.tenancy_created_on_expert_agent:
                old_tenancy_notes = "Tenancy Created On Expert Agent"
                notes_dict.append(old_tenancy_notes)
                instance.tenancy_created_on_expert_agent_date = (
                    datetime.date.today()
                )

            instance.save()

            phases = lettings_progression_percentage(property_process.id)

            phase_one = phases.get("phase_1")
            if phase_one > 99:
                lettings_prog_phase.phase_1 = True
                lettings_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = LettingsProgressionPhaseOneForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/lettings_progression/phase_one_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def lettings_phase_two(request, propertyprocess_id):
    """
    Ajax URL for phase two lettings progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    lettings_prog_phase = get_object_or_404(
        LettingsProgressionPhase,
        lettings_progression=property_process.lettings_progression.id,
    )

    progression = property_process.lettings_progression

    old_ref = progression.references_passed
    old_gas = progression.gas_safety_certificate
    old_elec = progression.electrical_certificate
    old_epc = progression.epc_certificate
    old_tenancy = progression.tenancy_certificate_sent

    if request.method == "POST":
        form = LettingsProgressionPhaseTwoForm(
            request.POST, instance=progression
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated lettings progression."
            )

            notes_dict = []

            if old_ref != instance.references_passed:
                old_ref_notes = "References Passed"
                notes_dict.append(old_ref_notes)
                instance.references_passed_date = datetime.date.today()

            if old_gas != instance.gas_safety_certificate:
                old_gas_notes = "Gas Safety Certificate"
                notes_dict.append(old_gas_notes)
                instance.gas_safety_certificate_date = datetime.date.today()

            if old_elec != instance.electrical_certificate:
                old_elec_notes = "Electrical Installation Certificate"
                notes_dict.append(old_elec_notes)
                instance.electrical_certificate_date = datetime.date.today()

            if old_epc != instance.epc_certificate:
                old_epc_notes = "Energy Performance Certificate"
                notes_dict.append(old_epc_notes)
                instance.epc_certificate_date = datetime.date.today()

            if old_tenancy != instance.tenancy_certificate_sent:
                old_tenancy_notes = "Tenancy Agreement Sent For Signature"
                notes_dict.append(old_tenancy_notes)
                instance.tenancy_certificate_sent_date = datetime.date.today()

            instance.save()

            phases = lettings_progression_percentage(property_process.id)

            phase_two = phases.get("phase_2")
            if phase_two > 99:
                lettings_prog_phase.phase_2 = True
                lettings_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = LettingsProgressionPhaseTwoForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "propertyprocess": property_process,
    }
    data["html_modal"] = render_to_string(
        "properties/lettings_progression/phase_two_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def lettings_phase_three(request, propertyprocess_id):
    """
    Ajax URL for phase three lettings progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    lettings_prog_phase = get_object_or_404(
        LettingsProgressionPhase,
        lettings_progression=property_process.lettings_progression.id,
    )

    progression = property_process.lettings_progression

    old_tenancy = progression.tenancy_agreement_signed
    old_invoice = progression.tenant_invoice_sent
    old_move_in_funds = progression.move_in_funds_received
    old_prescribed = progression.prescribed_info_and_statutory_docs_sent

    if request.method == "POST":
        form = LettingsProgressionPhaseThreeForm(
            request.POST, instance=progression
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated lettings progression."
            )

            notes_dict = []

            if old_tenancy != instance.tenancy_agreement_signed:
                old_tenancy_notes = "Tenancy Agreement Signed"
                notes_dict.append(old_tenancy_notes)
                instance.tenancy_agreement_signed_date = datetime.date.today()

            if old_invoice != instance.tenant_invoice_sent:
                old_invoice_notes = "Tenancy Invoice Sent"
                notes_dict.append(old_invoice_notes)
                instance.tenant_invoice_sent_date = datetime.date.today()

            if old_move_in_funds != instance.move_in_funds_received:
                old_move_in_funds_notes = "Move In Funds Received"
                notes_dict.append(old_move_in_funds_notes)
                instance.move_in_funds_received_date = datetime.date.today()

            if (
                old_prescribed
                != instance.prescribed_info_and_statutory_docs_sent
            ):
                old_prescribed_notes = "Prescribed Info & Statutory Docs Sent"
                notes_dict.append(old_prescribed_notes)
                instance.prescribed_info_and_statutory_docs_sent_date = (
                    datetime.date.today()
                )
            instance.save()

            phases = lettings_progression_percentage(property_process.id)

            phase_three = phases.get("phase_3")
            if phase_three > 99:
                lettings_prog_phase.phase_3 = True
                lettings_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = LettingsProgressionPhaseThreeForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
        "propertyprocess": property_process,
    }
    data["html_modal"] = render_to_string(
        "properties/lettings_progression/phase_three_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def lettings_phase_four(request, propertyprocess_id):
    """
    Ajax URL for phase four lettings progression
    """
    data = dict()

    property_process = get_object_or_404(
        PropertyProcess, id=propertyprocess_id
    )

    lettings_prog_phase = get_object_or_404(
        LettingsProgressionPhase,
        lettings_progression=property_process.lettings_progression.id,
    )

    progression = property_process.lettings_progression

    old_deposit = progression.deposit_registered_with_tds
    old_landlord = progression.landlord_invoices_sent_to_ea
    old_right_to_rent = progression.right_to_rent

    if request.method == "POST":
        form = LettingsProgressionPhaseFourForm(
            request.POST, instance=progression
        )
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            history_description = (
                f"{request.user.get_full_name()} has "
                "updated lettings progression."
            )

            notes_dict = []

            if old_deposit != instance.deposit_registered_with_tds:
                old_deposit_notes = "Deposit Registered With TDS"
                notes_dict.append(old_deposit_notes)
                instance.deposit_registered_with_tds_date = (
                    datetime.date.today()
                )

            if old_landlord != instance.landlord_invoices_sent_to_ea:
                old_landlord_notes = "Landlord Invoices Sent To EA"
                notes_dict.append(old_landlord_notes)
                instance.landlord_invoices_sent_to_ea_date = (
                    datetime.date.today()
                )

            if old_right_to_rent != instance.right_to_rent:
                old_right_to_rent_notes = "Right To Rent"
                notes_dict.append(old_right_to_rent_notes)
                instance.right_to_rent_date = datetime.date.today()

            instance.save()

            phases = lettings_progression_percentage(property_process.id)

            phase_four = phases.get("phase_4")
            print(phase_four)
            if phase_four > 99:
                print("In The If")
                lettings_prog_phase.phase_4 = True
                lettings_prog_phase.save()

            notes = "The following has been marked as complete, "

            for i, note in enumerate(notes_dict):
                if len(notes_dict) == 1:
                    notes += note
                    notes += "."
                else:
                    if i == len(notes_dict) - 1:
                        notes += note
                        notes += "."
                    elif i == len(notes_dict) - 2:
                        notes += note
                        notes += " and "
                    else:
                        notes += note
                        notes += ", "

            history = PropertyHistory.objects.create(
                propertyprocess=property_process,
                type=PropertyHistory.PROGRESSION,
                description=history_description,
                notes=notes,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )

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
        form = LettingsProgressionPhaseFourForm(
            instance=progression,
        )

    context = {
        "form": form,
        "propertyprocess_id": propertyprocess_id,
    }
    data["html_modal"] = render_to_string(
        "properties/lettings_progression/phase_four_modal.html",
        context,
        request=request,
    )

    return JsonResponse(data)
