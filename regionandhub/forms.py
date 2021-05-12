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
    validate_min=True
)
