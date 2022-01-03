from django.db import models
from django.db.models.signals import pre_save

from boards.functions import unique_property_ref_generator
from common.models import UpdatedAndCreated
from properties.models import PropertyProcess


class Boards(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "-created",
        ]
        verbose_name = "Board"
        verbose_name_plural = "Boards"

    propertyprocess = models.OneToOneField(
        PropertyProcess, on_delete=models.CASCADE, related_name="board"
    )
    propertyref = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
        editable=False
    )
    signmaster_id = models.CharField(
        null=True,
        blank=True,
        editable=False,
        max_length=200
    )
    created_on_signmaster = models.BooleanField(
        default=False
    )

    def __str__(self):
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 is None
        ):
            property_address = "%s, %s" % (
                self.propertyprocess.property.postcode,
                self.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.propertyprocess.property.postcode,
                self.propertyprocess.property.address_line_1,
                self.propertyprocess.property.address_line_2,
            )
        return property_address


def pre_save_create_property_ref(sender, instance, *args, **kwargs):
    if not instance.propertyref:
        instance.propertyref = unique_property_ref_generator(instance)


pre_save.connect(pre_save_create_property_ref, sender=Boards)


class BoardsInfo(UpdatedAndCreated):
    class Meta:
        ordering = []
        verbose_name = "Board Info"
        verbose_name_plural = "Boards Info"

    boards = models.OneToOneField(
        Boards, on_delete=models.CASCADE, related_name="board_info"
    )

    def __str__(self):
        if (
            self.boards.propertyprocess.property.address_line_2 == ""
            or self.boards.propertyprocess.property.address_line_2 is None
        ):
            property_address = "%s, %s" % (
                self.boards.propertyprocess.property.postcode,
                self.boards.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.boards.propertyprocess.property.postcode,
                self.boards.propertyprocess.property.address_line_1,
                self.boards.propertyprocess.property.address_line_2,
            )
        return property_address
