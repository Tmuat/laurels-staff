from django import forms

from lettings.models import (
    Maintenance,
    MaintenanceNotes,
    Gas,
    EPC,
    Electrical,
    Renewals
)
from properties.widgets import DateInput
from users.models import Profile


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = (
            "type",
            "status",
            "managed_by",
            "billing_status",
            "reported_by",
            "target_start_date",
            "actual_start_date",
            "target_completion_date",
            "actual_completion_date",
            "summary",
            "details",
            "contractor",
            "cost",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        self.fields["managed_by"].queryset = Profile.objects.filter(
            user__is_active=True
        ).order_by("user__first_name")
        labels = {
            "type": "Type",
            "status": "Status",
            "managed_by": "Managed By",
            "billing_status": "Billing Status",
            "reported_by": "Reported By",
            "target_start_date": "Target Start Date",
            "actual_start_date": "Actual Start Date",
            "target_completion_date": "Target Completion Date",
            "actual_completion_date": "Actual Completion Date",
            "summary": "Summary",
            "details": "Details",
            "contractor": "Contractor",
            "cost": "Cost",
        }

        self.fields["target_start_date"].widget = DateInput()
        self.fields["actual_start_date"].widget = DateInput()
        self.fields["target_completion_date"].widget = DateInput()
        self.fields["actual_completion_date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class MaintenanceNotesForm(forms.ModelForm):
    class Meta:
        model = MaintenanceNotes
        fields = (
            "notes",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "notes": "Notes",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class EPCForm(forms.ModelForm):
    class Meta:
        model = EPC
        fields = (
            "date",
            "expiry",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "date": "Date Added",
            "expiry": "Expiry",
        }

        self.fields["date"].widget = DateInput()
        self.fields["expiry"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class ElectricalForm(forms.ModelForm):
    class Meta:
        model = Electrical
        fields = (
            "date",
            "expiry",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "date": "Date Added",
            "expiry": "Expiry",
        }

        self.fields["date"].widget = DateInput()
        self.fields["expiry"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class GasForm(forms.ModelForm):
    class Meta:
        model = Gas
        fields = (
            "date",
            "expiry",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "date": "Date Added",
            "expiry": "Expiry",
        }

        self.fields["date"].widget = DateInput()
        self.fields["expiry"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class RenewalDateForm(forms.ModelForm):
    class Meta:
        model = Renewals
        fields = (
            "renewal_date",
        )

    def __init__(self, *args, **kwargs):
        """
        Add new labels and order foreign key field
        """
        super().__init__(*args, **kwargs)
        labels = {
            "renewal_date": "Next Renewal Date",
        }

        self.fields["renewal_date"].widget = DateInput()

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label
