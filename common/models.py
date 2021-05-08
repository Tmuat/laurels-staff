import uuid

from django.db import models


class UpdatedAndCreated(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True)
    updated_by = models.CharField(max_length=100, blank=True)
