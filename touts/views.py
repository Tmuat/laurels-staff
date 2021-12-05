from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from common.decorators import director_required


@director_required
@staff_member_required
@otp_required
@login_required
def area_list(request):
    """
    A view to show paginated lists of all touting areas in the system; including
    searching and filtering.
    """

    # properties_list = PropertyProcess.objects.select_related(
    #     "property",
    # ).prefetch_related(
    #     "employee",
    #     "hub",
    #     "history",
    # )
    # query = None
    # status = None
    # sector = None
    # archive = False

    # if request.GET:
    #     if "archive" in request.GET:
    #         archive = request.GET["archive"]
    #         if archive == "true":
    #             archive = True
    #     if "status" in request.GET:
    #         status = request.GET["status"]
    #         if status == "potential":
    #             properties_list = (
    #                 properties_list.exclude(macro_status=3)
    #                 .exclude(macro_status=4)
    #                 .exclude(macro_status=5)
    #             )
    #         elif status == "live":
    #             properties_list = (
    #                 properties_list.exclude(macro_status=0)
    #                 .exclude(macro_status=1)
    #                 .exclude(macro_status=2)
    #                 .exclude(macro_status=4)
    #                 .exclude(macro_status=5)
    #             )
    #         elif status == "deal":
    #             properties_list = (
    #                 properties_list.exclude(macro_status=0)
    #                 .exclude(macro_status=1)
    #                 .exclude(macro_status=2)
    #                 .exclude(macro_status=3)
    #                 .exclude(macro_status=5)
    #             )
    #         elif status == "complete":
    #             properties_list = (
    #                 properties_list.exclude(macro_status=0)
    #                 .exclude(macro_status=1)
    #                 .exclude(macro_status=2)
    #                 .exclude(macro_status=3)
    #                 .exclude(macro_status=4)
    #             )
    #     if "sector" in request.GET:
    #         sector = request.GET["sector"]
    #         properties_list = properties_list.filter(sector=sector)
    #     if "query" in request.GET:
    #         query = request.GET["query"]
    #         if not query:
    #             return redirect(reverse("properties:property_list"))

    #         queries = (
    #             Q(property__postcode__icontains=query)
    #             | Q(property__address_line_1__icontains=query)
    #             | Q(property__address_line_2__icontains=query)
    #         )
    #         properties_list = properties_list.filter(queries)

    # if archive is False:
    #     properties_list = properties_list.exclude(macro_status=-1)

    # properties_list_length = len(properties_list)

    # page = request.GET.get("page", 1)

    # paginator = Paginator(properties_list, 16)
    # last_page = paginator.num_pages

    # try:
    #     properties = paginator.page(page)
    # except PageNotAnInteger:
    #     properties = paginator.page(1)
    # except EmptyPage:
    #     properties = paginator.page(paginator.num_pages)

    context = {
        # "properties": properties,
        # "last_page": last_page,
        # "properties_length": properties_list_length,
        # "query": query,
        # "status": status,
        # "sector": sector,
        # "filter": filter,
        # "archive": archive,
    }

    template = "touts/area_list.html"

    return render(request, template, context)
