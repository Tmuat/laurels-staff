from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, reverse, redirect

from properties.models import PropertyProcess


def property_list(request):

    properties_list = PropertyProcess.objects.all() \
        .select_related(
            "property",
        ) \
        .prefetch_related(
            "employee",
            "hub",
            "history",
        )
    query = None
    status = None

    if request.GET:
        if "status" in request.GET:
            status = request.GET["status"]
            properties_list = properties_list.exclude(
                macro_status="comp"
            ).exclude(macro_status="withd")
        if "query" in request.GET:
            query = request.GET["query"]
            if not query:
                return redirect(reverse("properties:property_list"))

            queries = Q(property__postcode__icontains=query) | Q(
                property__address_line_1__icontains=query
            )
            properties_list = properties_list.filter(queries)

    properties_list_length = len(properties_list)

    page = request.GET.get("page", 1)

    paginator = Paginator(properties_list, 12)
    last_page = paginator.num_pages

    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        "properties": properties,
        "last_page": last_page,
        "properties_length": properties_list_length,
        "query": query,
        "status": status,
    }

    template = "properties/property_list.html"

    return render(request, template, context)
