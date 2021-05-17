from django.urls import path

from invitations.views import (
    invitation_home,
    invite_user,
    validate_email_invite,
    users_add_targets,
)


app_name = "invitations"
urlpatterns = [
    path("", invitation_home, name="invitations"),
    path("invite-user/", invite_user, name="invite_user"),
    path("check-user/", validate_email_invite, name="check_user"),
    path(
        "user-targets/<invitation_key>/",
        users_add_targets,
        name="targets_user",
    ),
    path(
        "accept/<invitation_key>/",
        users_add_targets,
        name="accept_invitation",
    ),
]
