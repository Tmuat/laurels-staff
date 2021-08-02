from django import forms
from django.utils.translation import gettext_lazy as _

from invitations.models import UserInvitations
from regionandhub.models import Hub
from users.models import UserTargets


class UserInvitationsForm(forms.ModelForm):
    class Meta:
        model = UserInvitations
        fields = (
            "email",
            "first_name",
            "last_name",
            "director",
            "is_staff",
            "hub",
            "employee_targets",
            "personal_comm",
        )
        labels = {
            "is_staff": _("Admin"),
        }

    hub = forms.ModelMultipleChoiceField(
        queryset=Hub.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "director":
                self.fields[field].label = ""
            elif field == "is_staff":
                self.fields[field].label = ""
            elif field == "hub":
                self.fields[field].label = ""
            elif field == "employee_targets":
                self.fields[field].label = ""
            elif field == "personal_comm":
                self.fields[field].label = "Personal Commision"


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
            "valuations",
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
