from django import forms
from django.utils.translation import gettext_lazy as _


from regionandhub.models import Region


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ("name",)
        labels = {
            "name": _("Region Name"),
        }
