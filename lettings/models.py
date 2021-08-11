from django.db import models

from common.models import UpdatedAndCreated
from properties.models import PropertyProcess, InstructionLettingsExtra


class ManagedProperties(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Managed Property"
        verbose_name_plural = "Managed Properties"

    BOOL_CHOICES = [(True, "Yes"), (False, "No")]

    SERVICE_LEVEL = [
        (InstructionLettingsExtra.INTRO, "Intro Only"),
        (InstructionLettingsExtra.RENTCOLLECT, "Rent Collect"),
        (InstructionLettingsExtra.FULLYMANAGED, "Fully Managed"),
    ]

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="managed_properties",
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
            "managed_property__propertyprocess__property__postcode",
            "managed_property__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Renewals"
        verbose_name_plural = "Renewals"

    managed_property = models.ForeignKey(
        ManagedProperties, on_delete=models.CASCADE, related_name="renewals"
    )
    renewed_on = models.DateField(null=True, blank=False)
    renewal_date = models.DateField(null=False, blank=False)

    def __str__(self):
        if (
            self.managed_property.propertyprocess.property.address_line_2 == ""
            or self.managed_property.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.managed_property.propertyprocess.property.postcode,
                self.managed_property.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.managed_property.propertyprocess.property.postcode,
                self.managed_property.propertyprocess.property.address_line_1,
                self.managed_property.propertyprocess.property.address_line_2,
            )
        return property_address


class SecondTwelve(UpdatedAndCreated):
    class Meta:
        ordering = [
            "-date",
            "managed_property__propertyprocess__property__postcode",
            "managed_property__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Second Twelve"
        verbose_name_plural = "Second Twelve's"

    managed_property = models.ForeignKey(
        ManagedProperties, on_delete=models.CASCADE,
        related_name="second_twelve"
    )
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        if (
            self.managed_property.propertyprocess.property.address_line_2 == ""
            or self.managed_property.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.managed_property.propertyprocess.property.postcode,
                self.managed_property.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.managed_property.propertyprocess.property.postcode,
                self.managed_property.propertyprocess.property.address_line_1,
                self.managed_property.propertyprocess.property.address_line_2,
            )
        return property_address

