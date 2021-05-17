from django_otp.decorators import otp_required

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from common.functions import quarter_year_calc
from invitations.forms import UserInvitationsForm
from invitations.models import UserInvitations
from users.forms import UserTargetsFormset
from users.models import UserTargetsByYear


@staff_member_required
@otp_required
@login_required
def invitation_home(request):
    invitations = UserInvitations.objects.all()
    active_invitations = invitations.filter(accepted=False).count()
    current_year = quarter_year_calc()

    context = {
        "invitations": invitations,
        "active_invitations": active_invitations,
        "current_year": current_year,
    }

    template = "invitations/invitation_list_view.html"

    return render(request, template, context)


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
            for hub in form.cleaned_data["hub"]:
                instance.hub.add(hub)
            instance.save()

            instance.send_invitation(request)

            if instance.employee_targets is True:
                data["targets"] = True
                data["invitation_key"] = instance.key
            else:
                data["targets"] = False

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
        pass
    else:
        form = UserInvitationsForm()

    context = {
        "form": form,
    }
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
        "is_taken": UserInvitations.objects.filter(
            email__iexact=email
        ).exists()
    }
    return JsonResponse(data)


@staff_member_required
@otp_required
@login_required
def users_add_targets(request, invitation_key):
    """
    Ajax URL for adding users targets to invitation model.
    """
    data = dict()
    invitation_instance = get_object_or_404(
        UserInvitations, key=invitation_key
    )

    if request.method == "POST":
        formset = UserTargetsFormset(
            request.POST, request.FILES, instance=invitation_instance
        )
        selected_year = request.POST.get("year")
        if formset.is_valid():
            instances = formset.save(commit=False)
            for count, instance in enumerate(instances):
                instance.year = selected_year
                quarter = count + 1
                instance.quarter = f"q{quarter}"
                instance.created_by = request.user.get_full_name()
                instance.updated_by = request.user.get_full_name()
                instance.save()
            UserTargetsByYear.objects.create(
                year=selected_year,
                targets_set=True,
                user_invitation=invitation_instance,
                created_by=request.user.get_full_name(),
                updated_by=request.user.get_full_name(),
            )
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
            context = {
                "formset": formset,
                "invitation_instance": invitation_instance,
            }
            data["html_large_modal"] = render_to_string(
                "invitations/includes/add_user_targets.html",
                context,
                request=request,
            )
    else:
        formset = UserTargetsFormset(instance=invitation_instance)
        context = {
            "formset": formset,
            "invitation_instance": invitation_instance,
        }
        data["html_large_modal"] = render_to_string(
            "invitations/includes/add_user_targets.html",
            context,
            request=request,
        )

    return JsonResponse(data)
