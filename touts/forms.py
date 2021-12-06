from django import forms

from touts.models import (
    Area,
)


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = (
            "area_code",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "area_code": "Area Code (Press Enter To Check If Unique)",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class AreaEditForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = (
            "area_code",
            "is_active"
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "area_code": "Area Code (Press Enter To Check If Unique)",
            "is_active": "Is Active?"
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label
