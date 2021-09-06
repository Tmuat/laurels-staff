from regionandhub.models import Hub


def active_hubs(request):
    return {
        "hubs": Hub.objects.filter(is_active=True),
    }
