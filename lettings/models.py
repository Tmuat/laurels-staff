from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from common.models import UpdatedAndCreated
from properties.models import PropertyProcess, InstructionLettingsExtra


class LettingProperties(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Lettings Property"
        verbose_name_plural = "Lettings Properties"

    BOOL_CHOICES = [(True, "Yes"), (False, "No")]

    SERVICE_LEVEL = [
        (InstructionLettingsExtra.INTRO, "Intro Only"),
        (InstructionLettingsExtra.RENTCOLLECT, "Rent Collect"),
        (InstructionLettingsExtra.FULLYMANAGED, "Fully Managed"),
    ]

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="lettings_properties",
    )
    lettings_service_level = models.CharField(
        max_length=40, null=True, blank=True, choices=SERVICE_LEVEL
    )
    is_active = models.BooleanField(choices=BOOL_CHOICES, default=True)

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


class Renewals(UpdatedAndCreated):
    class Meta:
        ordering = [
            "-renewed_on",
            "lettings_properties__propertyprocess__property__postcode",
            "lettings_properties__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Renewals"
        verbose_name_plural = "Renewals"

    lettings_properties = models.ForeignKey(
        LettingProperties, on_delete=models.CASCADE, related_name="renewals"
    )
    renewed_on = models.DateField(null=True, blank=False)
    renewal_date = models.DateField(null=False, blank=False)

    def __str__(self):
        if (
            self.lettings_properties.propertyprocess.property.address_line_2
            == ""
            or self.lettings_properties.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
                self.lettings_properties.propertyprocess.property.address_line_2,
            )
        return property_address


class SecondTwelve(UpdatedAndCreated):
    class Meta:
        ordering = [
            "-date",
            "lettings_properties__propertyprocess__property__postcode",
            "lettings_properties__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Second Twelve"
        verbose_name_plural = "Second Twelve's"

    lettings_properties = models.ForeignKey(
        LettingProperties,
        on_delete=models.CASCADE,
        related_name="second_twelve",
    )
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        if (
            self.lettings_properties.propertyprocess.property.address_line_2
            == ""
            or self.lettings_properties.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
                self.lettings_properties.propertyprocess.property.address_line_2,
            )
        return property_address


class EPC(UpdatedAndCreated):
    class Meta:
        ordering = [
            "-date",
            "lettings_properties__propertyprocess__property__postcode",
            "lettings_properties__propertyprocess__property__address_line_1",
        ]
        verbose_name = "EPC"
        verbose_name_plural = "EPC"

    lettings_properties = models.ForeignKey(
        LettingProperties, on_delete=models.CASCADE, related_name="epc"
    )
    date = models.DateField(null=False, blank=False)
    expiry = models.DateField(null=False, blank=False)

    def __str__(self):
        if (
            self.lettings_properties.propertyprocess.property.address_line_2
            == ""
            or self.lettings_properties.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
                self.lettings_properties.propertyprocess.property.address_line_2,
            )
        return property_address


class Gas(UpdatedAndCreated):
    class Meta:
        ordering = [
            "-date",
            "lettings_properties__propertyprocess__property__postcode",
            "lettings_properties__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Gas"
        verbose_name_plural = "Gas"

    lettings_properties = models.ForeignKey(
        LettingProperties, on_delete=models.CASCADE, related_name="gas"
    )
    date = models.DateField(null=False, blank=False)
    expiry = models.DateField(null=False, blank=False)

    def __str__(self):
        if (
            self.lettings_properties.propertyprocess.property.address_line_2
            == ""
            or self.lettings_properties.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
                self.lettings_properties.propertyprocess.property.address_line_2,
            )
        return property_address


class Electrical(UpdatedAndCreated):
    class Meta:
        ordering = [
            "-date",
            "lettings_properties__propertyprocess__property__postcode",
            "lettings_properties__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Electrical"
        verbose_name_plural = "Electrical"

    lettings_properties = models.ForeignKey(
        LettingProperties, on_delete=models.CASCADE, related_name="electrical"
    )
    date = models.DateField(null=False, blank=False)
    expiry = models.DateField(null=False, blank=False)

    def __str__(self):
        if (
            self.lettings_properties.propertyprocess.property.address_line_2
            == ""
            or self.lettings_properties.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
                self.lettings_properties.propertyprocess.property.address_line_2,
            )
        return property_address
