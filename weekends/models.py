import uuid

from django.db import models

from regionandhub.models import Hub


class WeekendDays(models.Model):
    class Meta:
        ordering = ["start"]
        verbose_name = "Weekend Day"
        verbose_name_plural = "Weekend Days"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(null=False, blank=False, max_length=200)
    start = models.DateField(null=False)
    end = models.DateField(null=False)
    hub = models.ForeignKey(
        Hub, on_delete=models.CASCADE, related_name="weekend_hub"
    )

    def __str__(self):
        weekend_days = "%s %s" % (
            self.start.strftime("%d-%m-%Y"),
            self.title,
        )
        return weekend_days
