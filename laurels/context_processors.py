from regionandhub.models import Hub
from properties.models import GlobalFeatureToggles


def active_hubs(request):
    return {
        "hubs": Hub.objects.filter(is_active=True),
    }


def global_feature_toggles(request):
    return {
        "gft": GlobalFeatureToggles.objects.all().first(),
    }
