from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@otp_required
@login_required
def index(request):
    """A view to return the index page"""

    return render(request, "home/index.html")
