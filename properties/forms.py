from django import forms

from properties.models import Property, PropertyProcess, Valuation, Marketing
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
        fields = (
            "price_quoted",
            "fee_quoted",
            "valuer",
            "date"
        )

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
            "date": "Valuation Date"
        }

        self.fields['date'].widget = DateInput()

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
