from datetime import date

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
    ]

    STATUS = [
        (VALUATION, "Valuation"),
        (INSTRUCTION, "Instruction"),
        (VIEWING, "Viewing"),
        (DEAL, "Deal"),
        (COMPLETE, "Complete"),
        (WITHDRAWN, "Withdrawn"),
    ]
    sector = models.CharField(max_length=40, null=False, choices=SECTOR)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    macro_status = models.CharField(
        max_length=40, null=False, blank=False, choices=STATUS
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


class Valuation(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Valuation"
        verbose_name_plural = "Valuations"

    propertyprocess = models.OneToOneField(
        PropertyProcess, on_delete=models.CASCADE, related_name="valuation"
    )
    date = models.DateField(default=date.today)
    price_quoted = models.PositiveIntegerField()
    fee_quoted = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        if self.propertyprocess.property.address_line_2 == "":
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


class Instruction(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Instruction"
        verbose_name_plural = "Instructions"

    SOLE = "sole"
    MULTI = "multi"

    WEEKS16 = 16
    WEEKS12 = 12
    WEEKS10 = 10
    WEEKS8 = 8
    WEEKS6 = 6
    WEEKS4 = 4

    AGREEMENT_TYPE = [
        (SOLE, "Sole"),
        (MULTI, "Multi"),
    ]

    LENGTH_OF_CONTRACT = [
        (WEEKS16, "16 Weeks"),
        (WEEKS12, "12 Weeks"),
        (WEEKS10, "10 Weeks"),
        (WEEKS8, "8 Weeks"),
        (WEEKS6, "6 Weeks"),
        (WEEKS4, "4 Weeks (Multi Only)"),
    ]

    BOOL_CHOICES = [(True, "Yes"), (False, "No")]

    propertyprocess = models.OneToOneField(
        PropertyProcess, on_delete=models.CASCADE, related_name="instruction"
    )
    date = models.DateField(default=date.today)
    agreement_type = models.CharField(max_length=15, choices=AGREEMENT_TYPE)
    listing_price = models.PositiveIntegerField(null=False, blank=False)
    fee_agreed = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, blank=False
    )
    length_of_contract = models.IntegerField(
        null=False, blank=False, choices=LENGTH_OF_CONTRACT
    )
    marketing_board = models.BooleanField(choices=BOOL_CHOICES)

    def __str__(self):
        if self.propertyprocess.property.address_line_2 == "":
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


class InstructionLettingsExtra(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Instruction Lettings Extra"
        verbose_name_plural = "Instructions Lettings Extra"

    INTRO = "intro_only"
    RENTCOLLECT = "rent_collect"
    FULLYMANAGED = "fully_managed"
    FULLYMANAGEDRI = "fully_managed_ri"

    SERVICE_LEVEL = [
        (INTRO, "Intro Only"),
        (RENTCOLLECT, "Rent Collect"),
        (FULLYMANAGED, "Fully Managed"),
        (FULLYMANAGEDRI, "Fully Managed Rent Insurance Included"),
    ]

    TRUE_FALSE_CHOICES = [(True, "Yes"), (False, "No")]

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="instruction_letting_extra",
    )
    lettings_service_level = models.CharField(
        max_length=40, null=True, blank=True, choices=SERVICE_LEVEL
    )
    managed_property = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )

    def __str__(self):
        if self.propertyprocess.property.address_line_2 == "":
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
