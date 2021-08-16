from django.forms.widgets import TextInput


class DateInput(TextInput):
    input_type = "date"


class NumberInput(TextInput):
    input_type = "number"
