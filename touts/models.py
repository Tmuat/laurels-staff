from django.db import models

from common.models import UpdatedAndCreated


class ToutProperty(UpdatedAndCreated):
    class Meta:
        ordering = ["postcode", "address_line_1"]
        verbose_name = "Tout Property"
        verbose_name_plural = "Tout Properties"
        unique_together = ["postcode", "address_line_1", "address_line_2"]

    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False)
    postcode = models.CharField(max_length=8, null=False)

    def __str__(self):
        if self.address_line_2 == "" or self.address_line_2 == None:
            property_address = "%s, %s" % (self.postcode, self.address_line_1)
        else:
            property_address = "%s, %s, %s" % (
                self.postcode,
                self.address_line_1,
                self.address_line_2,
            )
        return property_address

    @property
    def calculate_str_length(self, **kwargs):
        if self.address_line_2 == "" or self.address_line_2 is None:
            property_address = "%s" % (self.address_line_1)
        else:
            property_address = "%s, %s" % (
                self.address_line_1,
                self.address_line_2,
            )
        return len(property_address)

    @property
    def address_lines(self):
        if self.address_line_2 == "" or self.address_line_2 is None:
            property_address = "%s" % (self.address_line_1)
        else:
            property_address = "%s, %s" % (
                self.address_line_1,
                self.address_line_2,
            )
        return property_address

    @property
    def address(self):
        if self.address_line_2 == "" or self.address_line_2 == None:
            property_address = "%s, %s" % (self.postcode, self.address_line_1)
        else:
            property_address = "%s, %s, %s" % (
                self.postcode,
                self.address_line_1,
                self.address_line_2,
            )
        return property_address


class Landlord(UpdatedAndCreated):
    class Meta:
        ordering = ["postcode", "address_line_1", "landlord_name"]
        verbose_name = "Tout Landlord"
        verbose_name_plural = "Tout Landlords"
        unique_together = ["postcode", "address_line_1", "address_line_2"]

    landlord_name = models.CharField(max_length=150, null=False, blank=False)
    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False)
    postcode = models.CharField(max_length=8, null=False)
    landlord_property = models.ForeignKey(
        ToutProperty,
        on_delete=models.CASCADE,
        related_name="landlord_property",
    )

    def __str__(self):
        if self.address_line_2 == "" or self.address_line_2 == None:
            property_address = "%s, %s" % (self.postcode, self.address_line_1)
        else:
            property_address = "%s, %s, %s" % (
                self.postcode,
                self.address_line_1,
                self.address_line_2,
            )
        return property_address

    @property
    def calculate_str_length(self, **kwargs):
        if self.address_line_2 == "" or self.address_line_2 is None:
            property_address = "%s" % (self.address_line_1)
        else:
            property_address = "%s, %s" % (
                self.address_line_1,
                self.address_line_2,
            )
        return len(property_address)

    @property
    def address_lines(self):
        if self.address_line_2 == "" or self.address_line_2 is None:
            property_address = "%s" % (self.address_line_1)
        else:
            property_address = "%s, %s" % (
                self.address_line_1,
                self.address_line_2,
            )
        return property_address

    @property
    def address(self):
        if self.address_line_2 == "" or self.address_line_2 == None:
            property_address = "%s, %s" % (self.postcode, self.address_line_1)
        else:
            property_address = "%s, %s, %s" % (
                self.postcode,
                self.address_line_1,
                self.address_line_2,
            )
        return property_address