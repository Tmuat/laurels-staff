import requests

from xml.etree.ElementTree import Element, SubElement, tostring

from django.shortcuts import render

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

# from boards.views import *
# board_types()
