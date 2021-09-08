from django import forms

from properties.models import LettingsProgression, SalesProgression
from users.models import Profile


class ProgressorForm(forms.ModelForm):
    class Meta:
        model = SalesProgression
        fields = ("primary_progressor",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)

        self.fields["primary_progressor"].queryset = Profile.objects.filter(
            user__is_active=True
        )

        labels = {
            "primary_progressor": "Primary Progressor",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label


class LettingsProgressorForm(forms.ModelForm):
    class Meta:
        model = LettingsProgression
        fields = ("primary_progressor",)

    def __init__(self, *args, **kwargs):
        """
        Add new labels
        """
        super().__init__(*args, **kwargs)

        self.fields["primary_progressor"].queryset = Profile.objects.filter(
            user__is_active=True
        )

        labels = {
            "primary_progressor": "Primary Progressor",
        }

        for field in self.fields:
            label = f"{labels[field]}"
            self.fields[field].label = label
