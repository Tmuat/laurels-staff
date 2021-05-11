from django.db import models

from common.models import UpdatedAndCreated


class Region(UpdatedAndCreated):
    class Meta:
        ordering = ["name"]
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    name = models.CharField(
        max_length=50, null=False, blank=False, unique=True
    )
    slug = models.SlugField(null=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_slug(self):
        return self.slug


class Hub(UpdatedAndCreated):
    class Meta:
        ordering = ["hub_name"]
        verbose_name = "Hub"
        verbose_name_plural = "Hubs"

    hub_name = models.CharField(
        max_length=50, null=False, blank=False, unique=True
    )
    slug = models.SlugField(null=False, unique=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="region",
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.hub_name

    def get_slug(self):
        return self.slug


class HubTargets(UpdatedAndCreated):
    class Meta:
        ordering = ["year", "quarter"]
        verbose_name = "Hub Target"
        verbose_name_plural = "Hub Targets"
        unique_together = ["year", "quarter", "hub_targets"]

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
    instructions = models.PositiveIntegerField(blank=False, null=False)
    reductions = models.PositiveIntegerField(blank=False, null=False)
    new_business = models.PositiveIntegerField(blank=False, null=False)
    exchange_and_move = models.PositiveIntegerField(blank=False, null=False)
    hub_targets = models.ForeignKey(
        Hub, related_name="hub_targets", on_delete=models.CASCADE
    )

    def __str__(self):
        hub_targets_name = str(self.hub_targets)
        return hub_targets_name or ""
