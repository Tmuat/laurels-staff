from django.db import models

from common.models import UpdatedAndCreated


class Area(UpdatedAndCreated):
    class Meta:
        ordering = ["postcode"]
        verbose_name = "Area"
        verbose_name_plural = "Areas"

    postcode = models.CharField(max_length=8, unique=True, null=False)

    def __str__(self):
        return self.postcode


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
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="area",
    )

    def __str__(self):
        if self.address_line_2 == "" or self.address_line_2 is None:
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
        if self.address_line_2 == "" or self.address_line_2 is None:
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
        ordering = ["landlord_property__postcode", "landlord_property__address_line_1", "landlord_name"]
        verbose_name = "Tout Landlord"
        verbose_name_plural = "Tout Landlords"

    landlord_name = models.CharField(max_length=150, null=False, blank=False)
    landlord_salutation = models.CharField(max_length=150, null=False, blank=False)
    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False)
    county = models.CharField(max_length=100, null=True)
    postcode = models.CharField(max_length=8, null=False)
    landlord_property = models.ForeignKey(
        ToutProperty,
        on_delete=models.CASCADE,
        related_name="landlord_property",
    )

    def __str__(self):
        if self.landlord_property.address_line_2 == "" or self.landlord_property.address_line_2 is None:
            property_address_and_landlord = "%s, %s (%s)" % (
                self.landlord_property.postcode,
                self.landlord_property.address_line_1,
                self.landlord_name
            )
        else:
            property_address_and_landlord = "%s, %s, %s (%s)" % (
                self.landlord_property.postcode,
                self.landlord_property.address_line_1,
                self.landlord_property.address_line_2,
                self.landlord_name
            )
        return property_address_and_landlord

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
        if self.address_line_2 == "" or self.address_line_2 is None:
            property_address = "%s, %s" % (self.postcode, self.address_line_1)
        else:
            property_address = "%s, %s, %s" % (
                self.postcode,
                self.address_line_1,
                self.address_line_2,
            )
        return property_address


class ToutLetter(UpdatedAndCreated):
    class Meta:
        ordering = [
            "landlord__landlord_property__postcode",
            "landlord__landlord_property__address_line_1",
            "landlord__landlord_name"
        ]
        verbose_name = "Tout Letter"
        verbose_name_plural = "Tout Letters"

    landlord = models.ForeignKey(
        Landlord,
        on_delete=models.CASCADE,
        related_name="landlord",
    )
    letter_one = models.BooleanField(default=False)
    letter_two = models.BooleanField(default=False)
    letter_three = models.BooleanField(default=False)
    letter_four = models.BooleanField(default=False)
    letter_five = models.BooleanField(default=False)
    letter_six = models.BooleanField(default=False)
    do_not_send = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    requested_no_contact = models.BooleanField(default=False)

    def __str__(self):
        if (
            self.landlord.landlord_property.address_line_2 == ""
            or self.landlord.landlord_property.address_line_2 is None):
            property_address_and_landlord = "%s, %s (%s)" % (
                self.landlord.landlord_property.postcode,
                self.landlord.landlord_property.address_line_1,
                self.landlord.landlord_name
            )
        else:
            property_address_and_landlord = "%s, %s, %s (%s)" % (
                self.landlord.landlord_property.postcode,
                self.landlord.landlord_property.address_line_1,
                self.landlord.landlord_property.address_line_2,
                self.landlord.landlord_name
            )
        return property_address_and_landlord
