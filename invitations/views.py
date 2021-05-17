from django_otp.decorators import otp_required

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView

from invitations.forms import UserInvitationsForm
from invitations.models import UserInvitations


@method_decorator(staff_member_required, name='dispatch')
@method_decorator(otp_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class InvitationListView(ListView):

    queryset = UserInvitations.objects.all()
    context_object_name = 'invitations'
    paginate_by = 100  # if pagination is desired
    template_name = "invitations/invitation_list_view.html"


@staff_member_required
@otp_required
@login_required
def invite_user(request):
    """
    Ajax URL for inviting a user.
    """
    data = dict()

    if request.method == "POST":
        form = UserInvitationsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user.get_full_name()
            instance.updated_by = request.user.get_full_name()
            instance.save()
            for hub in form.cleaned_data['hub']:
                instance.hub.add(hub)
            instance.save()

            if instance.employee_targets is True:
                print("True")
                data["targets"] = True
            else:
                data["targets"] = False

                print("False")

            data["form_is_valid"] = True

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
        else:
            data["form_is_valid"] = False
        pass
    else:
        form = UserInvitationsForm()

    context = {"form": form, }
    data["html_modal"] = render_to_string(
        "invitations/includes/invite_user.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def validate_email_invite(request):
    """
    Check that the email is unqiue for invitees
    """
    email = request.GET.get("email", None)
    data = {
        "is_taken": UserInvitations.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)
