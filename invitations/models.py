from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from common.models import UpdatedAndCreated
from regionandhub.models import Hub


class UserInvitations(UpdatedAndCreated):
    class Meta:
        ordering = [
            "invited",
        ]
        verbose_name = "User Invitation"
        verbose_name_plural = "User Invitations"

    key = models.CharField(max_length=64, unique=True, null=False)
    invited = models.DateTimeField(null=True)
    accepted = models.BooleanField(default=False, null=False)

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(
        _("first name"), max_length=30, blank=False, null=False
    )
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False, null=False
    )
    director = models.BooleanField(null=False, blank=True, default=False)
    is_staff = models.BooleanField(null=False, blank=True, default=False)
    hub = models.ManyToManyField(Hub)
    employee_targets = models.BooleanField(
        null=False, blank=False, default=False
    )
    invite_sent = models.BooleanField(null=False, default=False)

    def send_invitation(self, request, **kwargs):
        invite_url = reverse("invitations:accept_invitation", args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        context = kwargs
        context.update(
            {
                "invite_url": invite_url,
                "email": self.email,
                "key": self.key,
            }
        )

        invite = render_to_string(
            "invitations/email/email_invite.txt", context
        )

        try:
            send_mail(
                "Laurels Intranet Invitation",
                invite,
                '"Laurels No Reply" <admin@laurels.co.uk>',
                recipient_list=[
                    self.email,
                ],
                fail_silently=False,
            )
            self.invite_sent = True
            self.invited = timezone.now()
            self.save()
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

    def save(self, *args, **kwargs):
        """
        Override the original save method to create a unique key.
        """
        if not self.key:
            self.key = get_random_string(64).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
