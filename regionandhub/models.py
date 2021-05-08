from django.db import models

from common.models import UpdatedAndCreated


class Region(UpdatedAndCreated):
    class Meta:
        ordering = ["name"]
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
