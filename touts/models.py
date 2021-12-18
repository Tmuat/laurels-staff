from django.db import models

from common.models import UpdatedAndCreated


class Area(UpdatedAndCreated):
    class Meta:
        ordering = ["area_code"]
        verbose_name = "Area"
        verbose_name_plural = "Areas"

    area_code = models.CharField(max_length=8, unique=True, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.area_code


class ToutProperty(UpdatedAndCreated):
    class Meta:
        ordering = ["postcode", "address_line_1"]
        verbose_name = "Tout Property"
        verbose_name_plural = "Tout Properties"
        unique_together = ["postcode", "address_line_1", "address_line_2"]

    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False)
    county = models.CharField(max_length=100, null=True, blank=True)
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
    address_line_1 = models.CharField(max_length=150, null=False, blank=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False, blank=False)
    county = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=8, null=False, blank=False)
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


class MarketingInfo(UpdatedAndCreated):
    class Meta:
        ordering = [
            "landlord__landlord_property__postcode",
            "landlord__landlord_property__address_line_1",
            "landlord__landlord_name"
        ]
        verbose_name = "Marketing Information"
        verbose_name_plural = "Marketing Information"

    HOUSE_TERRACED = "house_terraced"
    HOUSE_END_TERRACE = "house_end_terrace"
    HOUSE_SEMI_DETACHED = "house_semi_detached"
    HOUSE_DETACHED = "house_detached"
    FLAT_MAISONETTE_GROUND = "maisonette_ground_floor"
    FLAT_MAISONETTE_TOP = "maisonette_top_floor"
    FLAT_GROUND_FLOOR = "flat_ground_floor"
    FLAT_UPPER_FLOOR = "flat_upper_floor"
    BUNGALOW_SEMI_DETACHED = "bungalow_semi_detached"
    BUNGALOW_DETACHED = "bungalow_detached"
    OTHER_COMMERCIAL = "commercial"
    OTHER_LAND = "land"
    OTHER_OTHER = "other"

    PROPERTY_TYPE = [
        (
            "House",
            (
                (HOUSE_TERRACED, "House - Terraced"),
                (HOUSE_END_TERRACE, "House - End of Terrace"),
                (HOUSE_SEMI_DETACHED, "House - Semi-Detached"),
                (HOUSE_DETACHED, "House - Detached"),
            ),
        ),
        (
            "Flat",
            (
                (FLAT_MAISONETTE_GROUND, "Maisonette - Ground Floor"),
                (FLAT_MAISONETTE_TOP, "Maisonette - Top Floor"),
                (FLAT_GROUND_FLOOR, "Flat - Ground Floor"),
                (FLAT_UPPER_FLOOR, "Flat - Upper Floors"),
            ),
        ),
        (
            "Bungalow",
            (
                (BUNGALOW_SEMI_DETACHED, "Bungalow - Semi-Detached"),
                (BUNGALOW_DETACHED, "Bungalow - Detached"),
            ),
        ),
        (
            "Other",
            (
                (OTHER_COMMERCIAL, "Commercial"),
                (OTHER_LAND, "Land"),
                (OTHER_OTHER, "Other"),
            ),
        ),
    ]

    NUMBER_BEDROOMS = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    ]

    landlord = models.ForeignKey(
        Landlord,
        on_delete=models.CASCADE,
        related_name="landlord",
    )
    property_type = models.CharField(
        max_length=25, null=False, choices=PROPERTY_TYPE
    )
    number_of_bedrooms = models.IntegerField(
        null=False, choices=NUMBER_BEDROOMS
    )
    marketed_from_date = models.DateField()
    offer = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )

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


class ToutLetter(UpdatedAndCreated):
    class Meta:
        ordering = [
            "marketing__landlord",
        ]
        verbose_name = "Tout Letter"
        verbose_name_plural = "Tout Letters"

    marketing = models.OneToOneField(
        MarketingInfo,
        on_delete=models.CASCADE,
        related_name="marketing_info",
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
            self.marketing.landlord.landlord_property.address_line_2 == ""
            or self.marketing.landlord.landlord_property.address_line_2 is None):
            property_address_and_landlord = "%s, %s (%s)" % (
                self.marketing.landlord.landlord_property.postcode,
                self.marketing.landlord.landlord_property.address_line_1,
                self.marketing.landlord.landlord_name
            )
        else:
            property_address_and_landlord = "%s, %s, %s (%s)" % (
                self.marketing.landlord.landlord_property.postcode,
                self.marketing.landlord.landlord_property.address_line_1,
                self.marketing.landlord.landlord_property.address_line_2,
                self.marketing.landlord.landlord_name
            )
        return property_address_and_landlord
