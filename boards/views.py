import requests

from xml.etree.ElementTree import Element, SubElement, tostring

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from boards.models import Boards
from laurels.settings.base import (
    BOARDS_URL,
    BOARDS_API_KEY,
    BOARDS_COMPANY_KEY
)


def board_types():

    xml_payload = Element("movements")

    movement = SubElement(xml_payload, "movement")

    branchcode = SubElement(movement, "branchcode")
    branchcode.text = "TEST172"
    propertyref = SubElement(movement, "propertyref")
    propertyref.text = ""
    vendorname = SubElement(movement, "vendorname")
    vendorname.text = "T Muat"
    boardtypeid = SubElement(movement, "boardtypeid")
    boardtypeid.text = "42462"
    movementtypeid = SubElement(movement, "movementtypeid")
    movementtypeid.text = "1"
    boardstatusid = SubElement(movement, "boardstatusid")
    boardstatusid.text = "1"
    noofboards = SubElement(movement, "noofboards")
    noofboards.text = "1"
    houseno = SubElement(movement, "houseno")
    houseno.text = "58"
    address1 = SubElement(movement, "address1")
    address1.text = "Fareham Avenue"
    address2 = SubElement(movement, "address2")
    address2.text = ""
    locality = SubElement(movement, "locality")
    locality.text = ""
    town = SubElement(movement, "town")
    town.text = "Rugby"
    county = SubElement(movement, "county")
    county.text = "Warwickshire"
    postcode = SubElement(movement, "postcode")
    postcode.text = "CV22 5HT"
    agentnotes = SubElement(movement, "agentnotes")
    agentnotes.text = "Please erect to the side of the house."

    payload = {
        'key': BOARDS_API_KEY,
        'branchcode': BOARDS_COMPANY_KEY,
        'overwriteExisting': True,
        'returnFullDetails': False,
    }

    # r = requests.get(BOARDS_URL + "getBoardTypes", params=payload)

    # r = requests.get(BOARDS_URL + "getMovementTypes", params=payload)

    # r = requests.get(BOARDS_URL + "getBoardStatuses", params=payload)

    r = requests.get(
        BOARDS_URL + "addMovements",
        data=tostring(xml_payload),
        params=payload
    )

    print(r.text)

    # print(tostring(xml_payload))

    return r


# def create_addMovements_xml(instance, form):
#     """
#     """

#     xml_payload = Element("movements")

#     movement = SubElement(xml_payload, "movement")

#     branchcode = SubElement(movement, "branchcode")
#     branchcode.text = BOARDS_COMPANY_KEY

#     propertyref = SubElement(movement, "propertyref")
#     propertyref.text = ""
#     vendorname = SubElement(movement, "vendorname")
#     vendorname.text = "T Muat"
#     boardtypeid = SubElement(movement, "boardtypeid")
#     boardtypeid.text = "42462"
#     movementtypeid = SubElement(movement, "movementtypeid")
#     movementtypeid.text = "1"
#     boardstatusid = SubElement(movement, "boardstatusid")
#     boardstatusid.text = "1"
#     noofboards = SubElement(movement, "noofboards")
#     noofboards.text = "1"
#     houseno = SubElement(movement, "houseno")
#     houseno.text = "Flat 5"
#     address1 = SubElement(movement, "address1")
#     address1.text = "Woodfield Court"
#     address2 = SubElement(movement, "address2")
#     address2.text = "Woodfield Avenue"
#     locality = SubElement(movement, "locality")
#     locality.text = ""
#     town = SubElement(movement, "town")
#     town.text = "Rugby"
#     county = SubElement(movement, "county")
#     county.text = "Warwickshire"
#     postcode = SubElement(movement, "postcode")
#     postcode.text = "CV22 5HT"
#     agentnotes = SubElement(movement, "agentnotes")
#     agentnotes.text = "Please erect to the side of the house."

#     return xml_payload


def new_board():

    payload = {
        'key': BOARDS_API_KEY,
        'branchcode': BOARDS_COMPANY_KEY,
        'overwriteExisting': True,
        'returnFullDetails': False,
    }

    r = requests.get(
        BOARDS_URL + "addMovements",
        data=tostring(xml_payload),
        params=payload
    )

    print(r.text)

    return r


# from boards.views import *
# board_types()

def board_modal_selector(selector):
    """
    A function to return the correct modal html
    template.
    """

    modals = {
        "add_new_board": "new_listing.html",
    }

    modal = modals[selector]

    return modal


def board_modal_controller(request, board_id):
    """
    Ajax URL for getting the board options modal.
    """

    data = dict()

    board_instance = get_object_or_404(
        Boards, id=board_id
    )

    modal = board_modal_selector("add_new_board")

    context = {
        "board_instance": board_instance,
    }
    data["html_modal"] = render_to_string(
        f"touts/includes/forms/{modal}",
        context,
        request=request,
    )

    return JsonResponse(data)
