from base64 import b32encode
from binascii import unhexlify
import django_otp
from django_otp import devices_for_user
from django_otp.oath import totp
from django_otp.plugins.otp_static.models import StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
import qrcode
from two_factor.utils import get_otpauth_url

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.views.decorators.cache import never_cache
from django.views.generic.base import View

from accounts.forms import CustomConfirmChangeForm, totp_digits
from accounts.utils import class_view_decorator


def logout_modal(request):
    """
    Provides a response for an ajax request, delivering the logout modal.
    """
    html_modal = render_to_string(
        "registration/includes/partial_logout.html",
        request=request,
    )
    return JsonResponse({"html_modal": html_modal})


@never_cache
def otp_remove(request):
    """
    Ajax URL for removing a TOTP device.
    """
    data = dict()

    if request.method == "POST":
        form = CustomConfirmChangeForm(request.POST)
        if form.is_valid():
            for device in devices_for_user(request.user):
                device.delete()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = CustomConfirmChangeForm()

    context = {"form": form}
    data["html_modal"] = render_to_string(
        "two_factor/includes/remove_device.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@never_cache
def otp_setup(request):
    """
    AJAX URL for setting up a TOTP device.
    """
    session_key_name = "django_two_factor-qr_secret_key"
    data = dict()
    no_error = True

    if request.method == "POST":
        """
        On post get the keys from the session.

        Post the key to totp to get back the token to be checked against.

        Check to see if they user token and validated token match.
        """
        session = request.session.get(session_key_name)

        for key in session:
            if key == "keys":
                hex_key = session[key]

        unhex_key = unhexlify(hex_key.encode())

        validated_token = totp(key=unhex_key)

        user_token = request.POST.get("token")

        if validated_token == int(user_token):
            device = TOTPDevice.objects.create(
                user=request.user,
                key=hex_key,
                tolerance=1,
                t0=0,
                step=30,
                drift=0,
                digits=totp_digits(),
                name="default",
            )

            django_otp.login(request, device)

            try:
                del request.session[session_key_name]
            except KeyError:
                pass

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
            no_error = False
    else:
        """
        Check to see if the session key is already in the session and clear it.
        Generate a key on get request and store it in the session. One key to 
        be used to check against the OTP link and one to create the QR code.
        """
        try:
            del request.session[session_key_name]
        except KeyError:
            pass

        session = request.session.get(session_key_name, {})

        key = random_hex(20)

        session["keys"] = key

        rawkey = unhexlify(key.encode("ascii"))
        b32key = b32encode(rawkey).decode("utf-8")

        session["b32key"] = b32key

        request.session[session_key_name] = session

    context = {"no_error": no_error, "QR_URL": reverse("qr")}
    data["html_modal"] = render_to_string(
        "two_factor/includes/setup.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@never_cache
def otp_backup(request):
    """
    AJAX URL for creating backup OTP numbers.
    """

    data = dict()

    number_of_tokens = 10

    if request.method == "POST":
        device = request.user.staticdevice_set.get_or_create(name="backup")[0]
        device.token_set.all().delete()
        for n in range(number_of_tokens):
            device.token_set.create(token=StaticToken.random_token())
        data["form_is_valid"] = True
    else:
        device = request.user.staticdevice_set.get_or_create(name="backup")[0]

    context = {
        "device": device,
    }
    data["html_modal"] = render_to_string(
        "two_factor/includes/backup.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@class_view_decorator(never_cache)
@class_view_decorator(login_required)
class QRGeneratorView(View):
    """
    View returns an SVG image with the OTP token information
    """

    http_method_names = ["get"]
    default_qr_factory = "qrcode.image.svg.SvgPathImage"
    session_key_name = "django_two_factor-qr_secret_key"

    # The qrcode library only supports PNG and SVG for now
    image_content_types = {
        "PNG": "image/png",
        "SVG": "image/svg+xml; charset=utf-8",
    }

    def get_issuer(self):
        return get_current_site(self.request).name

    def get(self, request, *args, **kwargs):
        # Get the data from the session
        try:
            session = self.request.session[self.session_key_name]
            for key in session:
                if key == "b32key":
                    key = session[key]
        except KeyError:
            raise Http404()

        # Get data for qrcode
        image_factory_string = getattr(
            settings, "TWO_FACTOR_QR_FACTORY", self.default_qr_factory
        )
        image_factory = import_string(image_factory_string)
        content_type = self.image_content_types[image_factory.kind]
        try:
            username = self.request.user.get_username()
        except AttributeError:
            username = self.request.user.username

        otpauth_url = get_otpauth_url(
            accountname=username,
            issuer=self.get_issuer(),
            secret=key,
            digits=totp_digits(),
        )

        # Make and return QR code
        img = qrcode.make(otpauth_url, image_factory=image_factory)
        resp = HttpResponse(content_type=content_type)
        img.save(resp)
        return resp
