from django_otp.decorators import otp_required

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from regionandhub.models import Hub
from users.models import Profile
from weekends.models import WeekendDays


@otp_required
@login_required
def weekend_working(request):
    """
    A view to show the weekend working page
    """

    hub = request.user.profile.hub.first().slug

    if "hub" in request.GET:
        hub = request.GET.get("hub")
        hub = Hub.objects.get(slug=hub)

    employees = Profile.objects.filter(hub=hub.id, user__is_active=True)

    weekend_days = WeekendDays.objects.all()

    context = {
        "hub": hub,
        "employees": employees,
        "weekend_days": weekend_days,
    }

    template = "weekends/weekend_working.html"

    return render(request, template, context)


def weekend_working_json(request, hub_slug):
    """
    Returns the weekend days as json to the js file
    """

    hub = get_object_or_404(Hub, slug=hub_slug)

    weekend_days = WeekendDays.objects.filter(
        hub=hub,
    )

    days = []

    for instance in weekend_days:
        day = {}
        day["title"] = instance.title
        day["start"] = instance.start
        day["end"] = instance.end
        day["className"] = "bg-success"
        day["id"] = instance.id
        days.append(day)

    return JsonResponse(days, safe=False)


def add_weekend_working(request):

    data = dict()

    if request.POST:
        hub_slug = request.POST.get("hub")
        hub = get_object_or_404(Hub, slug=hub_slug)

        title = request.POST.get("title")

        start = request.POST.get("start")

        WeekendDays.objects.create(
            title=title, hub=hub, start=start, end=start
        )

        data["is_valid"] = True

    return JsonResponse(data)


def delete_weekend_working(request):

    data = dict()

    if request.POST:
        selected_id = request.POST.get("id")
        WeekendDays.objects.get(id=selected_id).delete()

        data["is_valid"] = True

    return JsonResponse(data)
