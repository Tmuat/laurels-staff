from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from invitations.models import UserInvitations
from users.models import CustomUser, UserTargets


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "password1": "Password",
            "password2": "Repeat Password",
            "is_staff": "Is Staff?",
            "is_superuser": "Is Superuser?",
            "is_active": "Active?",
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs["placeholder"] = placeholder


class CustomUserChangeForm(UserChangeForm):
    """
    This code is taken from the following tutorial:
    https://testdriven.io/blog/django-custom-user-model/
    """

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")


class UserTargetsForm(forms.ModelForm):
    class Meta:
        model = UserTargets
        fields = (
            "conveyancing",
            "mortgages",
            "instructions",
            "reductions",
            "new_business",
            "exchange_and_move",
        )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False


UserTargetsFormset = forms.inlineformset_factory(
    UserInvitations,
    UserTargets,
    form=UserTargetsForm,
    extra=0,
    can_delete=False,
    min_num=4,
    validate_min=True,
)
