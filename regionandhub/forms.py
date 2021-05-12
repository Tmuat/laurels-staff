from django import forms
from django.utils.translation import gettext_lazy as _

from regionandhub.models import Region, Hub, HubTargets


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ("name",)
        labels = {
            "name": _("Region Name"),
        }


class RegionEditForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ("name", "is_active")
        labels = {
            "name": _("Region Name"),
            "is_active": _("Region Still Active?"),
        }

    def __init__(self, *args, **kwargs):
        super(RegionEditForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["id"] = "id_region_name"


class HubForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = ("hub_name", "region")
        labels = {
            "hub_name": _("Hub Name"),
            "region": _("Associated Region"),
        }

    def __init__(self, *args, **kwargs):
        super(HubForm, self).__init__(*args, **kwargs)
        self.fields["region"].queryset = Region.objects.filter(is_active=True)


class HubEditForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = ("hub_name", "region", "is_active")
        labels = {
            "hub_name": _("Hub Name"),
            "region": _("Associated Region"),
            "is_active": _("Hub Still Active?")
        }

    def __init__(self, *args, **kwargs):
        super(HubEditForm, self).__init__(*args, **kwargs)
        self.fields["region"].queryset = Region.objects.filter(is_active=True)
        self.fields["hub_name"].widget.attrs["id"] = "id_change_hub_name"


class HubTargetsForm(forms.ModelForm):
    class Meta:
        model = HubTargets
        fields = (
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


HubTargetsFormset = forms.inlineformset_factory(
    Hub,
    HubTargets,
    form=HubTargetsForm,
    extra=0,
    can_delete=False,
    min_num=4,
    validate_min=True,
)
