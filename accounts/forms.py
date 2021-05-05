from django_otp.forms import OTPAuthenticationForm


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
