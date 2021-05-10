from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from regionandhub.models import Region


@otp_required
@login_required
def hub_and_region(request):
    """A view to return the list screen for hub and region page"""

    regions = Region.objects.filter(is_active=True).prefetch_related("region")

    context = {"regions": regions}

    template = "regionandhub/management.html"

    return render(request, template, context)
