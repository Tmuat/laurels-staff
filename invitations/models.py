from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import UpdatedAndCreated
from regionandhub.models import Hub, HubTargets, HubTargetsYear


class UserInvitations(UpdatedAndCreated):
    class Meta:
        ordering = [
            "invited",
        ]
        verbose_name = "User Invitation"
        verbose_name_plural = "User Invitations"

    key = models.CharField(max_length=64, unique=True, null=False)
    invited = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, null=False)

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(
        _("first name"), max_length=30, blank=False, null=False
    )
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False, null=False
    )
    director = models.BooleanField(null=True, blank=True, default=False)
    is_staff = models.BooleanField(null=False, blank=True, default=False)
    hub = models.ManyToManyField(Hub)
    employee_targets = models.BooleanField(
        null=False, blank=False, default=False
    )
    hub_targets = models.OneToOneField(
        HubTargets,
        on_delete=models.CASCADE,
        related_name="invitation_hub_targets",
        null=True,
        blank=True,
    )
    hub_targets_year = models.OneToOneField(
        HubTargetsYear,
        on_delete=models.CASCADE,
        related_name="invitation_hub_targets_year",
        null=True,
        blank=True,
    )
