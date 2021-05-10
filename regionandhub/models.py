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
        Region, on_delete=models.CASCADE, null=False, blank=False
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.hub_name

    def get_slug(self):
        return self.slug
