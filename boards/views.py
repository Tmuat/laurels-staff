from django_otp.decorators import otp_required
import requests
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from boards.forms import (
    AddNewBoardSalesForm,
    AddNewBoardLettingsForm,
)
from boards.models import Boards
from laurels.settings.base import (
    BOARDS_URL,
    BOARDS_API_KEY,
    BOARDS_COMPANY_KEY
)


def board_types():

    # xml_payload = Element("movements")

    # movement = SubElement(xml_payload, "movement")

    # branchcode = SubElement(movement, "branchcode")
    # branchcode.text = "TEST172"
    # propertyref = SubElement(movement, "propertyref")
    # propertyref.text = ""
    # vendorname = SubElement(movement, "vendorname")
    # vendorname.text = "T Muat"
    # boardtypeid = SubElement(movement, "boardtypeid")
    # boardtypeid.text = "42462"
    # movementtypeid = SubElement(movement, "movementtypeid")
    # movementtypeid.text = "1"
    # boardstatusid = SubElement(movement, "boardstatusid")
    # boardstatusid.text = "1"
    # noofboards = SubElement(movement, "noofboards")
    # noofboards.text = "1"
    # houseno = SubElement(movement, "houseno")
    # houseno.text = "58"
    # address1 = SubElement(movement, "address1")
    # address1.text = "Fareham Avenue"
    # address2 = SubElement(movement, "address2")
    # address2.text = ""
    # locality = SubElement(movement, "locality")
    # locality.text = ""
    # town = SubElement(movement, "town")
    # town.text = "Rugby"
    # county = SubElement(movement, "county")
    # county.text = "Warwickshire"
    # postcode = SubElement(movement, "postcode")
    # postcode.text = "CV22 5HT"
    # agentnotes = SubElement(movement, "agentnotes")
    # agentnotes.text = "Please erect to the side of the house."

    payload = {
        'key': BOARDS_API_KEY,
        'branchcode': BOARDS_COMPANY_KEY,
        'propertyref': "893954367"
    }

    # r = requests.get(BOARDS_URL + "getBoardTypes", params=payload)

    # r = requests.get(BOARDS_URL + "getMovementTypes", params=payload)

    # r = requests.get(BOARDS_URL + "getBoardStatuses", params=payload)

    r = requests.get(BOARDS_URL + "getListings", params=payload)

    # r = requests.get(
    #     BOARDS_URL + "addMovements",
    #     data=tostring(xml_payload),
    #     params=payload
    # )

    print(r.text)

    # from boards.views import board_types
    # board_types()

    return r


def new_board(board_instance, form):

    xml_payload = Element("movements")
    movement = SubElement(xml_payload, "movement")

    branchcode = SubElement(movement, "branchcode")
    branchcode.text = BOARDS_COMPANY_KEY

    propertyref = SubElement(movement, "propertyref")
    propertyref.text = str(board_instance.propertyref)

    vendorname = SubElement(movement, "vendorname")
    vendorname.text = form.cleaned_data["vendor_name"]

    boardtypeid = SubElement(movement, "boardtypeid")
    if board_instance.propertyprocess.sector == "sales":
        boardtypeid.text = "42462"
    else:
        boardtypeid.text = "42463"

    movementtypeid = SubElement(movement, "movementtypeid")
    movementtypeid.text = "1"

    boardstatusid = SubElement(movement, "boardstatusid")
    boardstatusid.text = form.cleaned_data["boardstatusid"]

    noofboards = SubElement(movement, "noofboards")
    noofboards.text = "1"

    houseno = SubElement(movement, "houseno")
    houseno.text = ""
    houseno.text = form.cleaned_data["houseno"]

    address1 = SubElement(movement, "address1")
    address1.text = form.cleaned_data["address1"]

    address2 = SubElement(movement, "address2")
    address2.text = form.cleaned_data["address2"]

    locality = SubElement(movement, "locality")
    locality.text = ""

    town = SubElement(movement, "town")
    town.text = form.cleaned_data["town"]

    county = SubElement(movement, "county")
    county.text = form.cleaned_data["county"]

    postcode = SubElement(movement, "postcode")
    postcode.text = form.cleaned_data["postcode"]

    agentnotes = SubElement(movement, "agentnotes")
    agentnotes.text = form.cleaned_data["agentnotes"]

    payload = {
        'key': BOARDS_API_KEY,
        'branchcode': BOARDS_COMPANY_KEY,
        'overwriteExisting': True,
        'returnFullDetails': False,
    }

    board_request = requests.post(
        BOARDS_URL + "addMovements",
        data=tostring(xml_payload),
        params=payload
    )

    return board_request


def parse_xml(request):
    """
    Parse the XML response for signmaster from string into XML
    """
    parsed_xml = fromstring(request.text)

    return parsed_xml


@otp_required
@login_required
def boards_menu(request, board_id):
    """
    Ajax URL for adding a board to the signmaster api.
    """
    data = dict()

    board_instance = get_object_or_404(
        Boards, id=board_id
    )

    context = {
        "board_instance": board_instance,
    }
    data["html_modal"] = render_to_string(
        "boards/includes/board_menu.html",
        context,
        request=request,
    )

    return JsonResponse(data)


@otp_required
@login_required
def add_board(request, board_id):
    """
    Ajax URL for adding a board to the signmaster api.
    """
    data = dict()

    board_instance = get_object_or_404(
        Boards, id=board_id
    )

    if request.method == "POST":
        if board_instance.propertyprocess.sector == "sales":
            form = AddNewBoardSalesForm(request.POST)
        else:
            form = AddNewBoardLettingsForm(request.POST)
        if form.is_valid():
            new_board_request = new_board(board_instance, form)
            parsed_xml = parse_xml(new_board_request)
            if parsed_xml.find("statuscode").text == "0001":
                data["html_board"] = render_to_string(
                    "boards/includes/responses/new_board_success.html",
                    request=request,
                )
                board_instance.created_on_signmaster = True
                board_instance.updated_by = request.user.get_full_name()
                board_instance.save()
            else:
                data["html_board"] = render_to_string(
                    "boards/includes/responses/new_board_error.html",
                    request=request,
                )
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        if board_instance.propertyprocess.sector == "sales":
            form = AddNewBoardSalesForm(
                initial={
                        "address1": board_instance.propertyprocess.property.address_line_1,
                        "address2": board_instance.propertyprocess.property.address_line_2,
                        "town": board_instance.propertyprocess.property.town,
                        "postcode": board_instance.propertyprocess.property.postcode,
                    }
            )
        else:
            form = AddNewBoardLettingsForm(
                initial={
                        "address1": board_instance.propertyprocess.property.address_line_1,
                        "address2": board_instance.propertyprocess.property.address_line_2,
                        "town": board_instance.propertyprocess.property.town,
                        "postcode": board_instance.propertyprocess.property.postcode,
                    }
            )

    context = {
        "form": form,
        "board_instance": board_instance,
    }
    data["html_modal"] = render_to_string(
        "boards/includes/new_listing.html",
        context,
        request=request,
    )

    return JsonResponse(data)
