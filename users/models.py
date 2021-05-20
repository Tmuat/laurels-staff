import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import UpdatedAndCreated
from invitations.models import UserInvitations
from regionandhub.models import Hub
from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    class Meta:
        ordering = ["email", "is_active"]
        verbose_name = "User & Profile"
        verbose_name_plural = "Users & Profiles"

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
    profile_picture = models.ImageField(null=True, blank=True)
    personal_comm = models.DecimalField(
        max_digits=4, decimal_places=2, default=10
    )
    office_comm = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )

    def __str__(self):
        return self.user.get_full_name()


class UserTargetsByYear(UpdatedAndCreated):
    class Meta:
        ordering = ["user", "year"]
        verbose_name = "User Target Set"
        verbose_name_plural = "User Targets Set"
        unique_together = ["year", "user"]

    Y_2021 = "2021"
    Y_2022 = "2022"
    Y_2023 = "2023"
    Y_2024 = "2024"
    Y_2025 = "2025"
    Y_2026 = "2026"

    YEAR_CHOICES = [
        (Y_2021, "2021"),
        (Y_2022, "2022"),
        (Y_2023, "2023"),
        (Y_2024, "2024"),
        (Y_2025, "2025"),
        (Y_2026, "2026"),
    ]

    year = models.CharField(
        max_length=4, blank=False, null=False, choices=YEAR_CHOICES
    )
    targets_set = models.BooleanField(default=False, null=False, blank=False)
    user = models.ForeignKey(
        CustomUser,
        related_name="user_targets_year_set",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user_invitation = models.ForeignKey(
        UserInvitations,
        related_name="user_invitation_targets_year",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        user_targets_name = str(self.user)
        user_invitation_name = str(self.user_invitation.email)
        if user_targets_name == "None":
            model_str = user_invitation_name
        else:
            model_str = user_targets_name
        return model_str


class UserTargets(UpdatedAndCreated):
    class Meta:
        ordering = ["year", "quarter"]
        verbose_name = "User Target"
        verbose_name_plural = "User Targets"
        unique_together = ["year", "quarter", "user_targets"]

    Q1 = "q1"
    Q2 = "q2"
    Q3 = "q3"
    Q4 = "q4"

    QUARTER_CHOICES = [
        (Q1, "Quarter 1"),
        (Q2, "Quarter 2"),
        (Q3, "Quarter 3"),
        (Q4, "Quarter 4"),
    ]

    Y_2021 = "2021"
    Y_2022 = "2022"
    Y_2023 = "2023"
    Y_2024 = "2024"
    Y_2025 = "2025"
    Y_2026 = "2026"

    YEAR_CHOICES = [
        (Y_2021, "2021"),
        (Y_2022, "2022"),
        (Y_2023, "2023"),
        (Y_2024, "2024"),
        (Y_2025, "2025"),
        (Y_2026, "2026"),
    ]

    year = models.CharField(
        max_length=4, blank=False, null=False, choices=YEAR_CHOICES
    )
    quarter = models.CharField(
        max_length=12, blank=False, null=False, choices=QUARTER_CHOICES
    )
    conveyancing = models.PositiveIntegerField(blank=False, null=False)
    mortgages = models.PositiveIntegerField(blank=False, null=False)
    instructions = models.PositiveIntegerField(blank=False, null=False)
    reductions = models.PositiveIntegerField(blank=False, null=False)
    new_business = models.PositiveIntegerField(blank=False, null=False)
    exchange_and_move = models.PositiveIntegerField(blank=False, null=False)
    user_targets = models.ForeignKey(
        CustomUser,
        related_name="user_targets",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user_invitation = models.ForeignKey(
        UserInvitations,
        related_name="user_invitation_targets",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        user_targets_name = str(self.user_targets)
        user_invitation_name = str(self.user_invitation.email)
        if user_targets_name == "None":
            model_str = user_invitation_name
        else:
            model_str = user_targets_name
        return model_str
