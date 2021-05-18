import datetime
from django_otp.decorators import otp_required

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from users.models import CustomUser
from common.decorators import anonymous_required
from common.functions import quarter_year_calc
from invitations.forms import UserInvitationsForm
from invitations.models import UserInvitations
from users.forms import UserTargetsFormset, CustomPasswordCreationForm
from users.models import UserTargetsByYear, Profile


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
    invitations = UserInvitations.objects.filter(email__iexact=email).exists()
    users = CustomUser.objects.filter(email__iexact=email).exists()

    taken = False

    if invitations is True or users is True:
        taken = True

    data = {"is_taken": taken}
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
        request_user = request.user.get_full_name()
        if formset.is_valid():
            instances = formset.save(commit=False)
            for count, instance in enumerate(instances):
                instance.year = selected_year
                quarter = count + 1
                instance.quarter = f"q{quarter}"
                instance.created_by = request_user
                instance.updated_by = request_user
                instance.save()
            UserTargetsByYear.objects.create(
                year=selected_year,
                targets_set=True,
                user_invitation=invitation_instance,
                created_by=request_user,
                updated_by=request_user,
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


@anonymous_required
def accept_invite(request, invitation_key):

    invitation_instance = get_object_or_404(
        UserInvitations, key=invitation_key
    )

    user_targets_year_qs = (
        invitation_instance.user_invitation_targets_year.all()
    )
    user_targets_qs = invitation_instance.user_invitation_targets.all()

    user = CustomUser.objects.filter(
        email__iexact=invitation_instance.email
    ).exists()
    expiry = invitation_instance.invited + datetime.timedelta(days=2)

    data = dict()
    valid = True

    if invitation_instance.accepted is True:
        valid = False
        data["invitation"] = "accepted"
    elif expiry <= timezone.now():
        valid = False
        data["invitation"] = "expired"
    elif user is True:
        valid = False
        data["invitation"] = "email in use"

    if request.method == "POST":
        form = CustomPasswordCreationForm(request.POST)
        if form.is_valid:
            instance_form = form.save(commit=False)
            instance_form.email = invitation_instance.email
            instance_form.first_name = invitation_instance.first_name
            instance_form.last_name = invitation_instance.last_name
            instance_form.is_staff = invitation_instance.is_staff
            instance_form.save()

            instance_profile = Profile.objects.create(
                user=instance_form,
                director=invitation_instance.director,
                employee_targets=invitation_instance.employee_targets,
                created_by=user_targets_qs.first().created_by,
                updated_by=user_targets_qs.first().created_by,
            )

            for hub in invitation_instance.hub.all():
                instance_profile.hub.add(hub)
            instance_profile.save()

            for target_year in user_targets_year_qs:
                target_year.user = instance_form
                target_year.save()

            for target in user_targets_qs:
                target.user_targets = instance_form
                target.save()

            invitation_instance.accepted = True
            invitation_instance.save()

            user = get_object_or_404(CustomUser, email=instance_form.email)

            login(request, user)
            return redirect("/")
        else:
            form = CustomPasswordCreationForm(request.POST)
    else:
        form = CustomPasswordCreationForm()

    context = {
        "valid": valid,
        "data": data,
        "invitation": invitation_instance,
        "form": form,
    }

    template = "invitations/accept_invitation.html"

    return render(request, template, context)
