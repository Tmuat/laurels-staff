from django import forms

from properties.models import (
    Property,
    Valuation
)


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ('postcode',
                  'address_line_1',
                  'address_line_2',
                  'town',
                  'property_type',
                  'property_style',
                  'number_of_bedrooms',
                  'tenure')

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
