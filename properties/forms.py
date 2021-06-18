from django import forms

from properties.models import (
    Property,
    PropertyProcess,
    Valuation,
    Instruction,
    Marketing,
    PropertyHistory,
    PropertyFees,
)
from properties.widgets import DateInput
from users.models import Profile


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = (
            "postcode",
            "address_line_1",
            "address_line_2",
            "town",
            "property_type",
            "property_style",
            "number_of_bedrooms",
            "tenure",
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
            "property_type": "Type",
            "property_style": "Style",
            "number_of_bedrooms": "Bedrooms",
            "tenure": "Tenure",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class PropertyProcessForm(forms.ModelForm):
    class Meta:
        model = PropertyProcess
        fields = (
            "sector",
            "employee",
            "hub",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        self.fields["employee"].queryset = Profile.objects.filter(
            user__is_active=True
        ).order_by("user__first_name")
        labels = {
            "sector": "Sector",
            "employee": "Employee",
            "hub": "Hub",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class ValuationForm(forms.ModelForm):
    class Meta:
        model = Valuation
        fields = ("price_quoted", "fee_quoted", "valuer", "date")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        self.fields["valuer"].queryset = Profile.objects.filter(
            user__is_active=True
        ).order_by("user__first_name")
        labels = {
            "price_quoted": "Price Quoted",
            "fee_quoted": "Fee Quoted",
            "valuer": "Valuer",
            "date": "Valuation Date",
        }

        self.fields["date"].widget = DateInput()

        self.fields["price_quoted"].widget.attrs["min"] = 0

        self.fields["fee_quoted"].widget.attrs["min"] = 0

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SellerMarketingForm(forms.ModelForm):
    class Meta:
        model = Marketing
        fields = (
            "hear_about_laurels",
            "contact_laurels",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "hear_about_laurels": "How Did The Seller Hear About Laurels?",
            "contact_laurels": "How Did The Seller Contact Laurels?",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class HistoryNotesForm(forms.ModelForm):
    class Meta:
        model = PropertyHistory
        fields = ("notes",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "notes": "Update Notes",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = (
            "date",
            "agreement_type",
            "listing_price",
            "fee_agreed",
            "length_of_contract",
            "marketing_board",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "date": "Date",
            "agreement_type": "Agreement Type",
            "listing_price": "Listing Price",
            "fee_agreed": "Fee Agreed",
            "length_of_contract": "Length of Contract",
            "marketing_board": "Marketing Board",
        }

        self.fields["date"].widget = DateInput()

        self.fields["listing_price"].widget.attrs["min"] = 0

        self.fields["fee_agreed"].widget.attrs["min"] = 0

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class FloorSpaceForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ("floor_space",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "floor_space": "Floor Space (Sq Ft)",
        }

        self.fields["floor_space"].widget.attrs["min"] = 0

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class ReductionForm(forms.ModelForm):
    class Meta:
        model = PropertyFees
        fields = (
            "date",
            "price",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "date": "Date",
            "price": "New Price (£)",
        }

        self.fields["date"].widget = DateInput()

        self.fields["price"].widget.attrs["min"] = 0

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label
