from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from regionandhub.models import Hub
from users.models import CustomUser, UserTargets, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "password1": "Password",
            "password2": "Repeat Password",
            "is_staff": "Is Staff?",
            "is_superuser": "Is Superuser?",
            "is_active": "Active?",
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs["placeholder"] = placeholder


class CustomPasswordCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("password1", "password2")
        exclude = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        """
        Remove help text.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = False


class CustomUserChangeForm(UserChangeForm):
    """
    This code is taken from the following tutorial:
    https://testdriven.io/blog/django-custom-user-model/
    """

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")


class UserTargetsForm(forms.ModelForm):
    class Meta:
        model = UserTargets
        fields = (
            "conveyancing",
            "mortgages",
            "instructions",
            "reductions",
            "new_business",
            "exchange_and_move",
            "valuations",
        )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False


UserTargetsFormset = forms.inlineformset_factory(
    CustomUser,
    UserTargets,
    form=UserTargetsForm,
    extra=0,
    can_delete=False,
    min_num=4,
    validate_min=True,
)


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "is_staff", "is_active")

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "is_staff":
                self.fields[field].label = ""
                self.fields[field].required = False
            elif field == "is_active":
                self.fields[field].label = ""
                self.fields[field].required = False
            else:
                self.fields[field].label = ""
            self.fields[field].help_text = None


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("director", "hub", "employee_targets", "personal_comm")

    director = forms.BooleanField()

    employee_targets = forms.BooleanField()

    hub = forms.ModelMultipleChoiceField(
        queryset=Hub.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "director":
                self.fields[field].label = ""
                self.fields[field].required = False
            if field == "employee_targets":
                self.fields[field].label = ""
                self.fields[field].required = False
            if field == "personal_comm":
                self.fields[field].label = ""
