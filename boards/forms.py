from django import forms


class AddNewBoardSalesForm(forms.Form):
    vendor_name = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Vendor Name"
    )

    houseno = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="House No."
    )

    address1 = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Address Line 1"
    )

    address2 = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=False,
        label="Address Line 2"
    )

    town = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Town"
    )

    county = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=False,
        label="County"
    )

    postcode = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Postcode"
    )

    agentnotes = forms.CharField(
        strip=True,
        widget=forms.Textarea(
            attrs={
                "rows": 2,
            }
        ),
        required=False,
        label="Agent Notes"
    )

    FOR_SALE = 1
    SOLD = 3
    SALE_AGREED = 5
    UNDER_OFFER = 6

    BOARD_STATUS = (
        (FOR_SALE, "For Sale"),
        (SOLD, "Sold"),
        (SALE_AGREED, "Sale Agreed"),
        (UNDER_OFFER, "Under Offer"),
    )

    boardstatusid = forms.ChoiceField(
        choices=BOARD_STATUS,
        label="Board Status"
    )


class AddNewBoardLettingsForm(forms.Form):
    vendor_name = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Vendor Name"
    )

    houseno = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="House No."
    )

    address1 = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Address Line 1"
    )

    address2 = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=False,
        label="Address Line 2"
    )

    town = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Town"
    )

    county = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        required=False,
        label="County"
    )

    postcode = forms.CharField(
        strip=True,
        widget=forms.TextInput(),
        label="Postcode"
    )

    agentnotes = forms.CharField(
        strip=True,
        widget=forms.Textarea(
            attrs={
                "rows": 2,
            }
        ),
        required=False,
        label="Agent Notes"
    )

    TO_LET = 2
    LET_BY = 4
    MANAGED_BY = 7

    BOARD_STATUS = (
        (TO_LET, "To Let"),
        (LET_BY, "Let By"),
        (MANAGED_BY, "Let & Managed By"),
    )

    boardstatusid = forms.ChoiceField(
        choices=BOARD_STATUS,
        label="Board Status"
    )
