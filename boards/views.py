import requests

from django.shortcuts import render

from laurels.settings.base import BOARDS_URL, BOARDS_API_KEY, BOARDS_COMPANY_KEY


def board_types():

    payload = {'key': BOARDS_API_KEY, 'branchcode': BOARDS_COMPANY_KEY}

    # r = requests.get(BOARDS_URL + "getBoardTypes", params=payload)

    # r = requests.get(BOARDS_URL + "getMovementTypes", params=payload)

    r = requests.get(BOARDS_URL + "getBoardStatuses", params=payload)

    print(r.text)

    return r


# from boards.views import *
# board_types()
