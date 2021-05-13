import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from common.models import UpdatedAndCreated
from regionandhub.models import Hub
from users.managers import CustomUserManager


class CustomUser(AbstractUser):

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(
        _("first name"), max_length=30, blank=False, null=False
    )
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False, null=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(UpdatedAndCreated):

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    director = models.BooleanField(null=True, blank=True, default=False)
    hub = models.ManyToManyField(Hub)
    employee_targets = models.BooleanField(
        null=False, blank=False, default=False
    )

    def __str__(self):
        return self.user.get_full_name()
