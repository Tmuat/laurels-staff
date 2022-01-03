from django.core.exceptions import ValidationError
from django import forms

from boards.models import BoardsInfo
from properties.widgets import DateInput


class AddNewBoardForm(forms.ModelForm):
    class Meta:
        model = BoardsInfo
        fields = (
            "vendor_name",
            "houseno",
            "address1",
            "address2",
            "town",
            "county",
            "postcode",
            "agentnotes",
            "boardstatusid",
        )

    vendor_name = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=True,
    )

    houseno = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=True,
    )

    address1 = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=True,
    )

    address2 = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=False,
    )

    town = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=True,
    )

    county = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=False,
    )

    postcode = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=True,
    )

    agentnotes = forms.CharField(
        strip=True,
        widget=forms.Textarea(
            attrs={
                "rows": 2,
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        labels = {
            "vendor_name": "Vendor Name",
            "houseno": "House No.",
            "address1": "Address 1",
            "address2": "Address 2",
            "town": "Town",
            "county": "County",
            "postcode": "Postcode",
            "agentnotes": "Agent Notes",
            "boardstatusid": "Board Status",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                choices = self.fields["boardstatusid"].choices
                if instance.boards.propertyprocess.sector == "sales":
                    del choices[0]
                    del choices[1]
                    del choices[2]
                    del choices[4]
                else:
                    del choices[0]
                    del choices[0]
                    del choices[1]
                    del choices[2]
                    del choices[2]
                field.choices = choices


class RetrieveBoardForm(forms.Form):

    date = forms.DateField(
        label=("Retrieval Date"),
        widget=DateInput(),
    )

    activate_date = forms.DateField(
        widget=forms.HiddenInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data["date"]
        activate_date = cleaned_data["activate_date"]

        if date < activate_date:
            raise ValidationError(
                "The date cannot be before the next actionable date!"
            )
