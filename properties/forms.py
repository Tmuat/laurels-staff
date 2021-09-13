from django import forms

from properties.models import (
    Property,
    PropertyProcess,
    Valuation,
    Instruction,
    InstructionLettingsExtra,
    InstructionChange,
    Marketing,
    PropertyHistory,
    PropertyFees,
    OffererDetails,
    OffererMortgage,
    OffererCash,
    OffererDetailsLettings,
    OfferLettingsExtra,
    Offer,
    Deal,
    DealExtraLettings,
    ExchangeMoveSales,
    ExchangeMoveLettings,
    SalesProgressionSettings,
    SalesProgression,
    LettingsProgression,
    LettingsProgressionSettings,
    PropertySellingInformation,
    ProgressionNotes,
    PropertyChain,
    LettingsLandlordOrLaurelsInformation,
)
from properties.widgets import DateInput, NumberInput
from regionandhub.models import Hub
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


class ReInstructionForm(forms.ModelForm):
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
            "date": "Back On The Market Date",
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


class InstructionLettingsExtraForm(forms.ModelForm):
    class Meta:
        model = InstructionLettingsExtra
        fields = ("lettings_service_level",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "lettings_service_level": "Service Level",
        }

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

    completed_offer_form = forms.BooleanField(required=False)

    class Meta:
        model = OffererDetails
        fields = ("full_name", "completed_offer_form", "funding", "status")
        widgets = {"funding": forms.RadioSelect}

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "full_name": "Full Name/s",
            "completed_offer_form": "Completed Offer Form?",
            "funding": "Funding Type",
            "status": "Status",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class OfferFormForm(forms.ModelForm):

    completed_offer_form = forms.BooleanField()

    class Meta:
        model = OffererDetails
        fields = ("completed_offer_form",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "completed_offer_form": "Completed Offer Form?",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class OffererLettingsForm(forms.ModelForm):

    completed_offer_form = forms.BooleanField(required=False)

    class Meta:
        model = OffererDetailsLettings
        fields = (
            "full_name",
            "completed_offer_form",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "full_name": "Full Name/s",
            "completed_offer_form": "Completed Offer Form?",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class OfferLettingsExtraForm(forms.ModelForm):
    class Meta:
        model = OfferLettingsExtra
        fields = (
            "proposed_move_in_date",
            "term",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "proposed_move_in_date": "Proposed Move In",
            "term": "Proposed Term",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label

            self.fields["proposed_move_in_date"].widget = DateInput()


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


class OfferLettingsForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("date", "offer", "status")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super(OfferLettingsForm, self).__init__(*args, **kwargs)
        labels = {
            "date": "Offer Date",
            "offer": "Offer Amount (£)",
            "status": "Offer Status",
        }

        self.fields["date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                choices = self.fields["status"].choices
                del choices[1]
                field.choices = choices


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


class OfferStatusLettingsForm(forms.ModelForm):
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

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                choices = self.fields["status"].choices
                del choices[1]
                field.choices = choices


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


class AnotherOfferLettingsForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("offerer_lettings_details", "date", "offer", "status")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "offerer_lettings_details": "Offerer",
            "date": "Offer Date",
            "offer": "Offer Amount (£)",
            "status": "Offer Status",
        }

        self.fields["date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                choices = self.fields["status"].choices
                del choices[1]
                field.choices = choices


class InstructionChangeForm(forms.ModelForm):
    class Meta:
        model = InstructionChange
        fields = ("agreement_type", "fee_agreed", "length_of_contract")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "agreement_type": "Agreement Type Change",
            "fee_agreed": "Fee Agreed Change",
            "length_of_contract": "Length of Contract Change",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class WithdrawalForm(forms.Form):

    NO_LONGER_MOVING = "no_longer_moving"
    OTHER_LAURELS_SUCCESS = "other_laurels_success"
    OTHER_AGENT = "other_agent"
    SOLD_OTHER_AGENT = "sold_other_agent"

    WITHDRAWN_REASON = (
        (NO_LONGER_MOVING, "No Longer Moving"),
        (OTHER_LAURELS_SUCCESS, "Other Laurels Success"),
        (OTHER_AGENT, "Going On The Market With Other Agent"),
        (SOLD_OTHER_AGENT, "Sold With Other Agent (Multi-Only)"),
    )
    withdrawal_reason = forms.ChoiceField(
        choices=WITHDRAWN_REASON,
        label=("Withdrawal Reason"),
    )
    date = forms.DateField(
        label=("Withdrawal Date"),
        widget=DateInput(),
    )


class DateForm(forms.Form):

    date = forms.DateField(
        label=("Date"),
        widget=DateInput(),
    )


class HubAndEmployeeForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Profile.objects.filter(
            user__is_active=True,
        ).order_by("user__first_name")
    )
    hub = forms.ModelChoiceField(
        queryset=Hub.objects.filter(
            is_active=True,
        ).order_by("hub_name")
    )


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ("date", "target_move_date", "offer_accepted")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "date": "Deal Date",
            "target_move_date": "Target Move Date",
            "offer_accepted": "Offer Being Accepted",
        }

        self.fields["date"].widget = DateInput()
        self.fields["target_move_date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class DealExtraForm(forms.ModelForm):
    class Meta:
        model = DealExtraLettings
        fields = (
            "term",
            "break_clause",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "term": "Agreed Term",
            "break_clause": "Agreed Break Clause",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class BuyerMarketingForm(forms.ModelForm):
    class Meta:
        model = Marketing
        fields = ("applicant_intro",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "applicant_intro": "How Was The Applicant Introduced",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SoldMarketingBoardForm(forms.Form):

    TRUE_FALSE_CHOICES = ((True, "Yes"), (False, "No"))

    sold_marketing_board = forms.ChoiceField(
        choices=TRUE_FALSE_CHOICES,
        label=("Sold Marketing Board"),
    )


class PropertyFeesForm(forms.ModelForm):
    class Meta:
        model = PropertyFees
        fields = ("price", "fee")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "price": "Price Agreed Change",
            "fee": "Fee Agreed Change",
        }

        self.fields["price"].widget.attrs["min"] = 0

        self.fields["fee"].widget.attrs["min"] = 0

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class ExchangeMoveSalesForm(forms.ModelForm):
    class Meta:
        model = ExchangeMoveSales
        fields = ("exchange_date", "completion_date")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "exchange_date": "Exchange Date",
            "completion_date": "Completion Date",
        }

        self.fields["exchange_date"].widget = DateInput()
        self.fields["completion_date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class ExchangeMoveLettingsForm(forms.ModelForm):
    class Meta:
        model = ExchangeMoveLettings
        fields = ("move_in_date", "first_renewal")

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)
        labels = {
            "move_in_date": "Move In Date",
            "first_renewal": "First Renewal Date",
        }

        self.fields["move_in_date"].widget = DateInput()
        self.fields["first_renewal"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SalesProgressionSettingsForm(forms.ModelForm):
    class Meta:
        model = SalesProgressionSettings
        fields = ("show_mortgage", "show_survey")

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "show_mortgage": "Show Mortgage Options",
            "show_survey": "Show Survey Options",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SalesProgressionPhaseOneForm(forms.ModelForm):
    class Meta:
        model = SalesProgression
        fields = (
            "buyers_aml_checks_and_sales_memo",
            "buyers_initial_solicitors_paperwork",
            "sellers_inital_solicitors_paperwork",
            "draft_contracts_recieved_by_buyers_solicitors",
            "searches_paid_for",
            "searches_ordered",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "buyers_aml_checks_and_sales_memo": "Buyers AML Checks & Sales Memo's Complete:",
            "buyers_initial_solicitors_paperwork": "Buyers Initial Paperwork Complete:",
            "sellers_inital_solicitors_paperwork": "Sellers Initial Paperwork Complete:",
            "draft_contracts_recieved_by_buyers_solicitors": "Draft Contracts Received By Buyers Solicitors:",
            "searches_paid_for": "Searches Paid For:",
            "searches_ordered": "Searches Ordered:",
        }

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SalesProgressionPhaseTwoForm(forms.ModelForm):
    class Meta:
        model = SalesProgression
        fields = (
            "mortgage_application_submitted",
            "mortgage_survey_arranged",
            "mortgage_offer_with_solicitors",
            "all_search_results_recieved",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "mortgage_application_submitted": "Mortgage Application Submitted:",
            "mortgage_survey_arranged": "Mortgage Survey Booked:",
            "mortgage_offer_with_solicitors": "Mortgage Offer With Solicitors:",
            "all_search_results_recieved": "All Search Results Received:",
        }

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SalesProgressionPhaseThreeForm(forms.ModelForm):
    class Meta:
        model = SalesProgression
        fields = (
            "enquiries_raised",
            "structural_survey_booked",
            "structural_survey_completed",
            "enquiries_answered",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "enquiries_raised": "Enquiries Raised:",
            "structural_survey_booked": "Structural Survey Booked:",
            "structural_survey_completed": "Structural Survey Completed:",
            "enquiries_answered": "Enquiries Answered:",
        }

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SalesProgressionPhaseFourForm(forms.ModelForm):
    class Meta:
        model = SalesProgression
        fields = (
            "additional_enquiries_raised",
            "all_enquiries_answered",
            "final_contracts_sent_out",
            "buyers_final_contracts_signed",
            "sellers_final_contracts_signed",
            "buyers_deposit_sent",
            "buyers_deposit_recieved",
            "completion_date_agreed",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "additional_enquiries_raised": "Additional Enquiries Raised:",
            "all_enquiries_answered": "All Enquiries Answered:",
            "final_contracts_sent_out": "Final Contracts Sent Out:",
            "buyers_final_contracts_signed": "Buyers Final Contracts Signed:",
            "sellers_final_contracts_signed": "Sellers Final Contracts Signed:",
            "buyers_deposit_sent": "Buyers Deposit Sent:",
            "buyers_deposit_recieved": "Buyers Deposit Received:",
            "completion_date_agreed": "Completion Date Agreed:",
        }

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class PropertySellingInformationForm(forms.ModelForm):
    class Meta:
        model = PropertySellingInformation
        fields = (
            "seller_name",
            "seller_phone",
            "seller_email",
            "buyer_name",
            "buyer_phone",
            "buyer_email",
            "seller_sol_name",
            "seller_sol_firm",
            "seller_sol_phone",
            "seller_sol_email",
            "buyer_sol_name",
            "buyer_sol_firm",
            "buyer_sol_phone",
            "buyer_sol_email",
            "broker_name",
            "broker_firm",
            "broker_phone",
            "broker_email",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "seller_name": "Name",
            "seller_phone": "Phone",
            "seller_email": "Email",
            "buyer_name": "Name",
            "buyer_phone": "Phone",
            "buyer_email": "Email",
            "seller_sol_name": "Name",
            "seller_sol_firm": "Firm",
            "seller_sol_phone": "Phone",
            "seller_sol_email": "Email",
            "buyer_sol_name": "Name",
            "buyer_sol_firm": "Firm",
            "buyer_sol_phone": "Phone",
            "buyer_sol_email": "Email",
            "broker_name": "Name",
            "broker_firm": "Firm",
            "broker_phone": "Phone",
            "broker_email": "Email",
        }

        self.fields["seller_phone"].widget = NumberInput()
        self.fields["buyer_phone"].widget = NumberInput()
        self.fields["seller_sol_phone"].widget = NumberInput()
        self.fields["buyer_sol_phone"].widget = NumberInput()
        self.fields["broker_phone"].widget = NumberInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class ProgressionNotesForm(forms.ModelForm):
    class Meta:
        model = ProgressionNotes
        fields = ("notes",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "notes": "",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class PropertyChainForm(forms.ModelForm):
    class Meta:
        model = PropertyChain
        fields = (
            "company",
            "branch",
            "address_line_1",
            "address_line_2",
            "town",
            "postcode",
            "chain_notes",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "company": "Company",
            "branch": "Branch",
            "address_line_1": "Address Line 1",
            "address_line_2": "Address Line 2",
            "town": "Town",
            "postcode": "Postcode",
            "chain_notes": "Notes",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class SalesProgressionResetForm(forms.Form):

    client_info = forms.BooleanField(
        required=False,
        label=("Reset Client Info"),
    )
    sales_progression = forms.BooleanField(
        required=False,
        label=("Reset Sales Progression"),
    )
    property_chain = forms.BooleanField(
        required=False,
        label=("Reset Property Chain"),
    )
    property_notes = forms.BooleanField(
        required=False,
        label=("Reset Progression Notes"),
    )


class LettingsProgressionSettingsForm(forms.ModelForm):
    class Meta:
        model = LettingsProgressionSettings
        fields = ("show_gas",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "show_gas": "Show Gas Certificate",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class LettingsProgressionPhaseOneForm(forms.ModelForm):
    class Meta:
        model = LettingsProgression
        fields = (
            "contact_touch_point_to_ll_and_tt",
            "reference_forms_sent_to_tenant",
            "compliance_form_sent_to_landlord",
            "google_drive_and_email_inbox",
            "tenancy_created_on_expert_agent",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "contact_touch_point_to_ll_and_tt": "Contact Touch Point To LL & TT:",
            "reference_forms_sent_to_tenant": "Referencing Forms Sent To Tenant:",
            "compliance_form_sent_to_landlord": "Compliance Form Received:",
            "google_drive_and_email_inbox": "Google Drive & Email Inbox Created:",
            "tenancy_created_on_expert_agent": "Tenancy Created On Expert Agent:",
        }

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class LettingsProgressionPhaseTwoForm(forms.ModelForm):
    class Meta:
        model = LettingsProgression
        fields = (
            "references_passed",
            "gas_safety_certificate",
            "gas_safety_certificate_expiry",
            "electrical_certificate",
            "electrical_certificate_expiry",
            "epc_certificate",
            "epc_certificate_expiry",
            "tenancy_certificate_sent",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "references_passed": "References Passed:",
            "gas_safety_certificate": "Gas Safety Certificate:",
            "gas_safety_certificate_expiry": "Gas Safety Certificate Expiry",
            "electrical_certificate": "Electrical Installation Certificate:",
            "electrical_certificate_expiry": "Electrical Certificate Expiry",
            "epc_certificate": "Energy Performance Certificate:",
            "epc_certificate_expiry": "EPC Certificate Expiry",
            "tenancy_certificate_sent": "Tenancy Agreement Sent For Signature",
        }

        self.fields["gas_safety_certificate_expiry"].widget = DateInput()
        self.fields["electrical_certificate_expiry"].widget = DateInput()
        self.fields["epc_certificate_expiry"].widget = DateInput()

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class LettingsProgressionPhaseThreeForm(forms.ModelForm):
    class Meta:
        model = LettingsProgression
        fields = (
            "tenancy_agreement_signed",
            "tenant_invoice_sent",
            "move_in_funds_received",
            "prescribed_info_and_statutory_docs_sent",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "tenancy_agreement_signed": "Tenancy Agreement Signed:",
            "tenant_invoice_sent": "Tenancy Invoice Sent:",
            "move_in_funds_received": "Move In Funds Received:",
            "prescribed_info_and_statutory_docs_sent": "Prescribed Info & Statutory Docs Sent:",
        }

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class LettingsProgressionPhaseFourForm(forms.ModelForm):
    class Meta:
        model = LettingsProgression
        fields = (
            "deposit_registered_with_tds",
            "landlord_invoices_sent_to_ea",
            "right_to_rent",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """

        super().__init__(*args, **kwargs)
        labels = {
            "deposit_registered_with_tds": "Deposit Registered With TDS:",
            "landlord_invoices_sent_to_ea": "Landlord Invoices Sent To EA:",
            "right_to_rent": "Right To Rent:",
        }

        instance = getattr(self, "instance", None)
        for model_field in instance._meta.get_fields():
            for field in self.fields:
                if model_field.name == field:
                    if getattr(instance, model_field.name) is True:
                        self.fields[field].disabled = True

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class EICRForm(forms.ModelForm):
    class Meta:
        model = LettingsLandlordOrLaurelsInformation
        fields = (
            "eicr_choice",
            "eicr_name",
            "eicr_phone",
            "eicr_email",
            "eicr_expected_completion",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "eicr_choice": "Organiser",
            "eicr_name": "Name or Firm",
            "eicr_phone": "Phone Number",
            "eicr_email": "Email",
            "eicr_expected_completion": "Expected Completion Date",
        }

        self.fields["eicr_expected_completion"].widget = DateInput()
        self.fields["eicr_phone"].widget = NumberInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class EPCForm(forms.ModelForm):
    class Meta:
        model = LettingsLandlordOrLaurelsInformation
        fields = (
            "epc_choice",
            "epc_name",
            "epc_phone",
            "epc_email",
            "epc_expected_completion",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "epc_choice": "Organiser",
            "epc_name": "Name or Firm",
            "epc_phone": "Phone Number",
            "epc_email": "Email",
            "epc_expected_completion": "Expected Completion Date",
        }

        self.fields["epc_expected_completion"].widget = DateInput()
        self.fields["epc_phone"].widget = NumberInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class GSCForm(forms.ModelForm):
    class Meta:
        model = LettingsLandlordOrLaurelsInformation
        fields = (
            "gsc_choice",
            "gsc_name",
            "gsc_phone",
            "gsc_email",
            "gsc_expected_completion",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "gsc_choice": "Organiser",
            "gsc_name": "Name or Firm",
            "gsc_phone": "Phone Number",
            "gsc_email": "Email",
            "gsc_expected_completion": "Expected Completion Date",
        }

        self.fields["gsc_expected_completion"].widget = DateInput()
        self.fields["gsc_phone"].widget = NumberInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class InventoryForm(forms.ModelForm):
    class Meta:
        model = LettingsLandlordOrLaurelsInformation
        fields = (
            "inventory_choice",
            "inventory_name",
            "inventory_phone",
            "inventory_email",
            "inventory_expected_completion",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "inventory_choice": "Organiser",
            "inventory_name": "Name or Firm",
            "inventory_phone": "Phone Number",
            "inventory_email": "Email",
            "inventory_expected_completion": "Expected Completion Date",
        }

        self.fields["inventory_expected_completion"].widget = DateInput()
        self.fields["inventory_phone"].widget = NumberInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class CleaningForm(forms.ModelForm):
    class Meta:
        model = LettingsLandlordOrLaurelsInformation
        fields = (
            "professional_clean_choice",
            "professional_clean_name",
            "professional_clean_phone",
            "professional_clean_email",
            "professional_clean_expected_completion",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """

        super().__init__(*args, **kwargs)
        labels = {
            "professional_clean_choice": "Organiser",
            "professional_clean_name": "Name or Firm",
            "professional_clean_phone": "Phone Number",
            "professional_clean_email": "Email",
            "professional_clean_expected_completion": "Expected Completion Date",
        }

        self.fields["professional_clean_expected_completion"].widget = DateInput()
        self.fields["professional_clean_phone"].widget = NumberInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label
