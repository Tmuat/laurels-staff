from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from properties.models import PropertyProcess


def property_list(request):

    properties_list = PropertyProcess.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(properties_list, 10)
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        "properties": properties,
    }

    template = "properties/property_list.html"

    return render(request, template, context)

