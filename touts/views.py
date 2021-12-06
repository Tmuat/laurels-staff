from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from common.decorators import director_required
from touts.forms import AreaForm, AreaEditForm
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
            instance = form.save(commit=False)

            instance.is_active = True
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
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


@director_required
@staff_member_required
@otp_required
@login_required
def area_edit(request, area_code):
    """
    Ajax URL for editing an area.
    """
    data = dict()

    area_code = get_object_or_404(Area, area_code=area_code)

    if request.method == "POST":
        form = AreaEditForm(request.POST, instance=area_code)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.updated_by = request.user.get_full_name()

            instance.save()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        form = AreaEditForm(instance=area_code)

    context = {
        "form": form,
        "instance": area_code
    }
    data["html_modal"] = render_to_string(
        "touts/includes/forms/edit_area.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@director_required
@staff_member_required
@otp_required
@login_required
def validate_area_code(request):
    """
    Check that the area code is unique prior to form submission
    """
    area_code = request.GET.get("area_code", None)
    print(area_code)
    data = {
        "is_taken": Area.objects.filter(area_code__iexact=area_code).exists()
    }
    return JsonResponse(data)


@director_required
@staff_member_required
@otp_required
@login_required
def tout_list(request):
    """
    A view to show paginated lists of all touting areas and the properties in the system; including filtering.
    """

    area_list = Area.objects.filter(is_active=True)

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

    template = "touts/tout_list.html"

    return render(request, template, context)
