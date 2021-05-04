from django.http import JsonResponse
from django.template.loader import render_to_string


def logout_modal(request):
    html_modal = render_to_string(
        'registration/includes/partial_logout.html',
        request=request,
    )
    return JsonResponse({'html_modal': html_modal})
