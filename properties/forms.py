from django import forms

from properties.models import (
    Property,
    PropertyProcess,
    Valuation,
    Instruction,
    Marketing,
    PropertyHistory,
    PropertyFees,
    OffererDetails,
    OffererMortgage,
    OffererCash,
    Offer,
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


class OffererForm(forms.ModelForm):

    completed_offer_form = forms.BooleanField()

    class Meta:
        model = OffererDetails
        fields = ("full_name", "completed_offer_form", "funding")
        widgets = {"funding": forms.RadioSelect}

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "full_name": "Full Name/s",
            "completed_offer_form": "Completed Offer Form?",
            "funding": "Funding Type",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class OffererMortgageForm(forms.ModelForm):
    class Meta:
        model = OffererMortgage
        fields = (
            "deposit_percentage",
            "verified_status",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "deposit_percentage": "Deposit Percentage",
            "verified_status": "Mortgage Verified Status",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class OffererCashForm(forms.ModelForm):
    class Meta:
        model = OffererCash
        fields = ("cash",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "cash": "Where is the cash coming from?",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("date", "offer", "status")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "date": "Offer Date",
            "offer": "Offer Amount (£)",
            "status": "Offer Status",
        }

        self.fields["date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class OfferStatusForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("status",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "status": "Offer Status",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class AnotherOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("offerer_details", "date", "offer", "status")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "offerer_details": "Offerer",
            "date": "Offer Date",
            "offer": "Offer Amount (£)",
            "status": "Offer Status",
        }

        self.fields["date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label
