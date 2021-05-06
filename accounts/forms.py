from binascii import unhexlify
from django_otp.forms import OTPAuthenticationForm
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice
from time import time

from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.utils import totp_digits


class CustomOTPAuthenticationForm(OTPAuthenticationForm):
    def __init__(self, *args, **kwargs):
        """
        Add custom label and remove auto-generated
        labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "otp_device": "OTP Device",
            "otp_token": "OTP Token*",
            "otp_challenge": "OTP Challenge",
        }

        for field in self.fields:
            if field == "otp_token":
                label = labels[field]
                self.fields[field].label = label


class CustomConfirmChangeForm(forms.Form):
    understand = forms.BooleanField(label=_("Yes, I Am Sure"))


