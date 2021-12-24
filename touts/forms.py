from django import forms
from django.forms import formset_factory

from properties.widgets import DateInput
from touts.models import (
    Area,
    ToutProperty,
    Landlord,
    MarketingInfo
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
            "address_line_1": "LL Address Line 1",
            "address_line_2": "LL Address Line 2",
            "town": "LL Town",
            "county": "LL County",
            "postcode": "LL Postcode"
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class AddLandlordExistingPropertyForm(forms.ModelForm):
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
            "landlord_property"
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
            "address_line_1": "LL Address Line 1",
            "address_line_2": "LL Address Line 2",
            "town": "LL Town",
            "county": "LL County",
            "postcode": "LL Postcode",
            "landlord_property": "Existing Property"
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class AddMarketingForm(forms.ModelForm):
    class Meta:
        model = MarketingInfo
        fields = (
            "property_type",
            "number_of_bedrooms",
            "marketed_from_date",
            "price",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "property_type": "Property Type",
            "number_of_bedrooms": "Number of Bedrooms",
            "marketed_from_date": "Marketed From Date",
            "price": "Price",
        }

        self.fields["price"].widget.attrs["min"] = 0
        self.fields["price"].widget.attrs["step"] = 1

        self.fields["marketed_from_date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class AddMarketingExistingLandlordForm(forms.ModelForm):
    class Meta:
        model = MarketingInfo
        fields = (
            "landlord",
            "property_type",
            "number_of_bedrooms",
            "marketed_from_date",
            "price",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "landlord": "Landlord",
            "property_type": "Property Type",
            "number_of_bedrooms": "Number of Bedrooms",
            "marketed_from_date": "Marketed From Date",
            "price": "Price",
        }

        self.fields["price"].widget.attrs["min"] = 0
        self.fields["price"].widget.attrs["step"] = 1

        self.fields["marketed_from_date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class ToutLetterForm(forms.Form):
    SENT = True
    NOT_SENT = False

    SENT_CHOICES = [
        (SENT, "Letter Sent"),
        (NOT_SENT, "Not Sent"),
    ]

    sent = forms.ChoiceField(
        choices=SENT_CHOICES,
        label="",
        initial=NOT_SENT,
        widget=forms.Select()
    )

    date = forms.DateField(
        label=(""),
        widget=DateInput(
            attrs={'disabled': True}
        ),
        required=False
    )


ToutLetterFormSet = formset_factory(
    ToutLetterForm,
    extra=6,
    can_delete=False,
    min_num=0,
    validate_min=True,
)
