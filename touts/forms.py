from django import forms

from touts.models import (
    Area,
    ToutProperty,
    Landlord
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


class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = ToutProperty
        fields = (
            "postcode",
            "address_line_1",
            "address_line_2",
            "town",
            "county",
            "area",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "postcode": "Postcode",
            "address_line_1": "Address Line 1",
            "address_line_2": "Address Line 2",
            "town": "Town",
            "county": "County",
            "area": "Area Code"
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label

        """
        Filter to active areas only
        """
        self.fields["area"].queryset = Area.objects.filter(is_active=True)


class AddLandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = (
            "landlord_name",
            "landlord_salutation",
            "address_line_1",
            "address_line_2",
            "town",
            "county",
            "postcode",
        )

    address_line_1 = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'id_ll_address_line_1'})
    )

    address_line_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'id_ll_address_line_2',
            }
        )
    )

    town = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'id_ll_town'})
    )

    county = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'id_ll_county'
            }
        )
    )

    postcode = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'id_ll_postcode'})
    )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "landlord_name": "Landlord Name",
            "landlord_salutation": "Landlord Salutation",
            "address_line_1": "Address Line 1",
            "address_line_2": "Address Line 2",
            "town": "Town",
            "county": "County",
            "postcode": "Postcode"
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label
