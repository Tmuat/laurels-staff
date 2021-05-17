from django import forms
from django.utils.translation import gettext_lazy as _

from invitations.models import UserInvitations
from regionandhub.models import Hub


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
