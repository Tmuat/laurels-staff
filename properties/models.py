from django.db import models

from common.models import UpdatedAndCreated
from regionandhub.models import Hub
from users.models import Profile


class Property(UpdatedAndCreated):
    class Meta:
        ordering = ["postcode", "address_line_1"]
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        unique_together = ["postcode", "address_line_1", "address_line_2"]

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

    MODERN = "modern"
    NEW_BUILD = "new_build"
    PERIOD = "period"

    FREEHOLD = "freehold"
    LEASHOLD = "leasehold"
    SHARE_OF_FREEHOLD = "share_of_freehold"

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

    PROPERTY_STYLE = [
        (MODERN, "Modern"),
        (NEW_BUILD, "New Build"),
        (PERIOD, "Period"),
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

    TENURE = [
        (FREEHOLD, "Freehold"),
        (LEASHOLD, "Leasehold"),
        (SHARE_OF_FREEHOLD, "Share of Freehold"),
    ]

    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False)
    postcode = models.CharField(max_length=8, null=False)
    property_type = models.CharField(
        max_length=25, null=False, choices=PROPERTY_TYPE
    )
    property_style = models.CharField(
        max_length=30, null=False, choices=PROPERTY_STYLE
    )
    number_of_bedrooms = models.CharField(
        max_length=50, null=False, choices=NUMBER_BEDROOMS
    )
    tenure = models.CharField(
        max_length=50, null=True, blank=False, choices=TENURE
    )
    floor_space = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        if self.address_line_2 == "":
            property_address = "%s, %s" % (self.postcode, self.address_line_1)
        else:
            property_address = "%s, %s, %s" % (
                self.postcode,
                self.address_line_1,
                self.address_line_2,
            )
        return property_address


class PropertyProcess(UpdatedAndCreated):
    class Meta:
        ordering = ["property__postcode", "property__address_line_1"]
        verbose_name = "Property Link"
        verbose_name_plural = "Property Links"

    LETTINGS = "lettings"
    SALES = "sales"

    VALUATION = "val"
    INSTRUCTION = "inst"
    VIEWING = "view"
    DEAL = "deal"
    COMPLETE = "comp"
    WITHDRAWN = "withd"

    SECTOR = [
        (LETTINGS, "Lettings"),
        (SALES, "Sales"),
        (INSTRUCTION, "Instruction"),
        (VIEWING, "Viewing"),
        (DEAL, "Deal"),
        (COMPLETE, "Complete"),
        (WITHDRAWN, "Withdrawn"),
    ]

    STATUS = [
        (VALUATION, "Valuation"),
    ]
    sector = models.CharField(max_length=40, null=False, choices=SECTOR)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    macro_status = models.CharField(
        max_length=40, null=False, blank=False, choices=SECTOR
    )
    hub = models.ForeignKey(
        Hub, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        if self.property.address_line_2 == "":
            property_address = "%s, %s" % (
                self.property.postcode,
                self.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.property.postcode,
                self.property.address_line_1,
                self.property.address_line_2,
            )
        return property_address
