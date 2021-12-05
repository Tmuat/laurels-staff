from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from common.decorators import director_required
from touts.forms import AreaForm
from touts.models import Area


@director_required
@staff_member_required
@otp_required
@login_required
def area_list(request):
    """
    A view to show paginated lists of all touting areas in the system; including
    searching and filtering.
    """

    area_list = Area.objects.all()

    active = True

    if request.GET:
        if "active" in request.GET:
            active = request.GET["active"]
            if active == "True":
                active = True
            elif active == "False":
                active = False

    if active is True:
        area_list = area_list.filter(is_active=True)

    page = request.GET.get("page", 1)

    paginator = Paginator(area_list, 16)
    last_page = paginator.num_pages

    try:
        area_list = paginator.page(page)
    except PageNotAnInteger:
        area_list = paginator.page(1)
    except EmptyPage:
        area_list = paginator.page(paginator.num_pages)

    context = {
        "area_list": area_list,
        "active": active,
        "last_page": last_page,
    }

    template = "touts/area_list.html"

    return render(request, template, context)


@director_required
@staff_member_required
@otp_required
@login_required
def area_add(request):
    """
    Ajax URL for adding an area.
    """
    data = dict()

    if request.method == "POST":
        form = AreaForm(request.POST)
        if form.is_valid():
            # instance = form.save(commit=False)
            # region_name = request.POST.get("name")

            # instance.slug = slugify(region_name)
            # instance.is_active = True
            # instance.created_by = request.user.get_full_name()
            # instance.updated_by = request.user.get_full_name()

            # instance.save()

            # data["form_is_valid"] = True

            # current_year = quarter_year_calc()
            # next_year = str(int(current_year) + 1)

            # regions = Region.objects.filter(is_active=True).prefetch_related(
            #     "region"
            # )
            # data["html_region_panels"] = render_to_string(
            #     "regionandhub/includes/panel.html",
            #     {
            #         "regions": regions,
            #         "current_year": current_year,
            #         "next_year": next_year,
            #     },
            # )
            # data["html_region_page_title"] = render_to_string(
            #     "regionandhub/includes/page-title.html", {"regions": regions}
            # )
            pass
        else:
            data["form_is_valid"] = False

    else:
        form = AreaForm()

    context = {"form": form}
    data["html_modal"] = render_to_string(
        "touts/includes/forms/add_area.html",
        context,
        request=request,
    )
    return JsonResponse(data)
