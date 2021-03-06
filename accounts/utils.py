from django.conf import settings
from django.utils.decorators import method_decorator


def class_view_decorator(function_decorator):
    """
    Converts a function based decorator into a class based decorator usable
    on class based Views.
    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    From: http://stackoverflow.com/a/8429311/58107
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


def totp_digits():
    """
    Returns the number of digits (as configured by the TWO_FACTOR_TOTP_DIGITS setting)
    for totp tokens. Defaults to 6
    """
    return getattr(settings, "TWO_FACTOR_TOTP_DIGITS", 6)
