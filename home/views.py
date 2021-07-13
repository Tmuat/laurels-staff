from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from properties.models import Offer
from regionandhub.models import Hub
from users.models import Profile


@otp_required
@login_required
def index(request):
    """A view to return the index page"""

    return render(request, "home/index.html")


def offer_board(request):
    """A view to return the offer_board page"""

    hubs = Hub.objects.filter(is_active=True)
    employees = Profile.objects.filter(
        employee_targets=True, user__is_active=True
    )

    offers = Offer.objects.exclude(propertyprocess__macro_status=4). \
        exclude(propertyprocess__macro_status=5). \
        exclude(status=Offer.REJECTED). \
        exclude(status=Offer.WITHDRAWN). \
        select_related(
            "propertyprocess",
            "propertyprocess__property"
        )
    print(len(offers))

    hub = None
    if "hub" in request.GET:
        selected_hub = request.GET.get("hub")
        hub = Hub.objects.get(slug=selected_hub)
        offers = offers.filter(propertyprocess__hub=hub)

    print(len(offers))

    user = None
    if "user" in request.GET:
        selected_user = request.GET.get("user")
        user = Profile.objects.get(id=selected_user)
        offers = offers.filter(propertyprocess__employee=user)

    print(len(offers))

    offers = offers.order_by("date")

    context = {
        "hubs": hubs,
        "selected_hub": hub,
        "employees": employees,
        "selected_user": user,
        "offers": offers,
    }

    return render(request, "home/offer_board.html", context)
