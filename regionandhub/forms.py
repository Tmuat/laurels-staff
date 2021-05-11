from django import forms
from django.utils.translation import gettext_lazy as _


from regionandhub.models import Region, Hub


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ("name",)
        labels = {
            "name": _("Region Name"),
        }


class HubForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = ("hub_name", "region")
        labels = {
            "hub_name": _("Hub Name"),
            "region": _("Associated Name"),
        }

    def __init__(self, *args, **kwargs):
        super(HubForm, self).__init__(*args, **kwargs)
        self.fields["region"].queryset = Region.objects.filter(is_active=True)
