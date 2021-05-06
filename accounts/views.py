from base64 import b32encode
from binascii import unhexlify
import django_otp
from django_otp import devices_for_user
from django_otp.util import random_hex
from two_factor.forms import (
    AuthenticationTokenForm, BackupTokenForm, DeviceValidationForm, MethodForm,
    PhoneNumberForm, PhoneNumberMethodForm, TOTPDeviceForm, YubiKeyDeviceForm,
)
from two_factor.forms import get_available_methods
from two_factor.utils import default_device

from django.conf import settings
from django.forms import Form
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, resolve_url
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

from accounts.forms import CustomConfirmChangeForm, CustomTOTPDeviceForm
from accounts.utils import class_view_decorator, IdempotentSessionWizardView


def logout_modal(request):
    html_modal = render_to_string(
        "registration/includes/partial_logout.html",
        request=request,
    )
    return JsonResponse({"html_modal": html_modal})


@never_cache
def otp_remove(request):
    data = dict()

    if request.method == 'POST':
        form = CustomConfirmChangeForm(request.POST)
        if form.is_valid():
            for device in devices_for_user(request.user):
                device.delete()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = CustomConfirmChangeForm()

    context = {'form': form}
    data['html_modal'] = render_to_string(
        "two_factor/includes/remove_device.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def otp_setup(request):
    key = random_hex(20)
    session_key_name = 'django_two_factor-qr_secret_key'
    data = dict()

    if request.method == 'POST':
        form = CustomTOTPDeviceForm(request.POST, user=request.user)
    else:
        form = CustomTOTPDeviceForm(key=key, user=request.user)
        rawkey = unhexlify(key.encode('ascii'))
        b32key = b32encode(rawkey).decode('utf-8')
        request.session[session_key_name] = b32key

    context = {
        'form': form,
        'QR_URL': reverse('qr')
    }
    data['html_modal'] = render_to_string(
        "two_factor/includes/setup.html",
        context,
        request=request,
    )
    return JsonResponse(data)

