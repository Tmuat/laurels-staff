from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, reverse, redirect

from properties.models import PropertyProcess


def property_list(request):

    properties_list = PropertyProcess.objects.all()
    query = None
    categories = None

    if request.GET:
        # if "category" in request.GET:
        #     categories = request.GET["category"].split(",")
        #     products = products.filter(category__name__in=categories)
        #     categories = Category.objects.filter(name__in=categories)

        if "query" in request.GET:
            query = request.GET["query"]
            if not query:
                return redirect(reverse("properties:property_list"))

            queries = (
                Q(property__postcode__icontains=query)
                | Q(property__address_line_1__icontains=query)
            )
            properties_list = properties_list.filter(queries)
    
    properties_list_length = len(properties_list)

    page = request.GET.get('page', 1)

    paginator = Paginator(properties_list, 10)
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
        "current_categories": categories,
    }

    template = "properties/property_list.html"

    return render(request, template, context)

