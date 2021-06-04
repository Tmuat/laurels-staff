from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

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

    LEGACY = [(True, "Legacy"), (False, "Not Legacy")]
    sector = models.CharField(max_length=40, null=False, choices=SECTOR)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="property"
    )
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    macro_status = models.CharField(
        max_length=40, null=False, blank=False, choices=STATUS
    )
    hub = models.ForeignKey(
        Hub, on_delete=models.CASCADE, null=False, blank=False
    )
    legacy_property = models.BooleanField(default=False, choices=LEGACY)

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


class PropertyHistory(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "-created",
        ]
        verbose_name = "Property History"
        verbose_name_plural = "Property History"

    PROPERTY_EVENT = "property_event"
    OFFER = "offer"
    PROGRESSION = "progression"
    MANAGEMENT = "management"
    OTHER = "other"

    TYPE = [
        (PROPERTY_EVENT, "Property Event"),
        (OFFER, "Offer"),
        (PROGRESSION, "Progression"),
        (MANAGEMENT, "Management"),
        (OTHER, "Other"),
    ]

    propertyprocess = models.ForeignKey(
        PropertyProcess, on_delete=models.CASCADE, related_name="history"
    )
    type = models.CharField(
        max_length=40, null=False, blank=False, choices=TYPE
    )
    description = models.CharField(max_length=400, null=False, blank=False)
    notes = models.TextField(null=True, blank=True)

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
    valuer = models.ForeignKey(Profile, on_delete=models.CASCADE)

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


class OffererDetails(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "full_name",
        ]
        verbose_name = "Offerer History"
        verbose_name_plural = "Offerer History"

    CASH = "cash"
    MORTGAGE = "mortgage"

    FUNDING = [(CASH, "Cash"), (MORTGAGE, "Mortgage")]

    COMPLETED = [(True, "Completed"), (False, "Incomplete")]

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="offerer_details",
    )
    full_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(blank=True)
    completed_offer_form = models.BooleanField(
        default=False, null=True, blank=False, choices=COMPLETED
    )
    funding = models.CharField(
        max_length=10, null=True, blank=False, choices=FUNDING
    )

    def __str__(self):
        if self.propertyprocess.property.address_line_2 == "":
            property_address = "%s, %s (%s)" % (
                self.propertyprocess.property.postcode,
                self.propertyprocess.property.address_line_1,
                self.full_name,
            )
        else:
            property_address = "%s, %s, %s (%s)" % (
                self.propertyprocess.property.postcode,
                self.propertyprocess.property.address_line_1,
                self.propertyprocess.property.address_line_2,
                self.full_name,
            )
        return property_address


class OffererMortgage(UpdatedAndCreated):
    class Meta:
        ordering = [
            "offerer_details__propertyprocess__property__postcode",
            "offerer_details__propertyprocess__property__address_line_1",
            "offerer_details__full_name",
        ]
        verbose_name = "Offerer Mortgage Details"
        verbose_name_plural = "Offerer Mortgage Details"

    PENDING = "pending"
    VERIFIEDMR = "verified_mr"
    MIP = "mip"
    UNABLE = "unable"

    VERI_CHOICES = [
        (PENDING, "Pending"),
        (VERIFIEDMR, "Verified By Mortgage Required"),
        (MIP, "Mortgage In Principle Seen"),
        (UNABLE, "Unable To Verify"),
    ]

    offerer_details = models.OneToOneField(
        OffererDetails,
        on_delete=models.CASCADE,
        related_name="offerer_mortgage_details",
    )
    deposit_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    verified = models.BooleanField(default=False, null=True)
    verified_status = models.CharField(
        max_length=50, null=False, blank=False, choices=VERI_CHOICES
    )

    def __str__(self):
        if self.offerer_details.propertyprocess.property.address_line_2 == "":
            property_address = "%s, %s (%s)" % (
                self.offerer_details.propertyprocess.property.postcode,
                self.offerer_details.propertyprocess.property.address_line_1,
                self.offerer_details.full_name,
            )
        else:
            property_address = "%s, %s, %s (%s)" % (
                self.offerer_details.propertyprocess.property.postcode,
                self.offerer_details.propertyprocess.property.address_line_1,
                self.offerer_details.propertyprocess.property.address_line_2,
                self.offerer_details.full_name,
            )
        return property_address


class OffererCash(UpdatedAndCreated):
    class Meta:
        ordering = [
            "offerer_details__propertyprocess__property__postcode",
            "offerer_details__propertyprocess__property__address_line_1",
            "offerer_details__full_name",
        ]
        verbose_name = "Offerer Cash Details"
        verbose_name_plural = "Offerer Cash Details"

    SAVINGS = "savings"
    SALEOFPROPERTY = "sale_of_property"
    GIFT = "gift"
    REMORTGAGE = "re_mortgage"

    CASH_CHOICES = [
        (SAVINGS, "Savings"),
        (SALEOFPROPERTY, "Sale of Property"),
        (GIFT, "Gift"),
        (REMORTGAGE, "Re-Mortgage"),
    ]

    offerer_details = models.OneToOneField(
        OffererDetails,
        on_delete=models.CASCADE,
        related_name="offerer_cash_details",
    )
    cash = models.CharField(
        max_length=50, null=False, blank=False, choices=CASH_CHOICES
    )

    def __str__(self):
        if self.offerer_details.propertyprocess.property.address_line_2 == "":
            property_address = "%s, %s (%s)" % (
                self.offerer_details.propertyprocess.property.postcode,
                self.offerer_details.propertyprocess.property.address_line_1,
                self.offerer_details.full_name,
            )
        else:
            property_address = "%s, %s, %s (%s)" % (
                self.offerer_details.propertyprocess.property.postcode,
                self.offerer_details.propertyprocess.property.address_line_1,
                self.offerer_details.propertyprocess.property.address_line_2,
                self.offerer_details.full_name,
            )
        return property_address


class Offer(UpdatedAndCreated):
    class Meta:
        ordering = [
            "offerer_details__propertyprocess__property__postcode",
            "offerer_details__propertyprocess__property__address_line_1",
            "offerer_details__full_name",
            "date",
        ]
        verbose_name = "Offer Details"
        verbose_name_plural = "Offer Details"

    GETTINGVERIFIED = "getting_verified"
    NEGOTIATING = "negotiating"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"

    STATUS = [
        (GETTINGVERIFIED, "Getting Verified"),
        (NEGOTIATING, "Negotiating"),
        (REJECTED, "Rejected"),
        (ACCEPTED, "Accepted"),
        (WITHDRAWN, "Withdrawn"),
    ]

    offerer_details = models.ForeignKey(
        OffererDetails,
        on_delete=models.CASCADE,
        related_name="offerdetails",
    )
    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="offer",
    )
    date = models.DateField(null=False, blank=False)
    offer = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    status = models.CharField(
        max_length=50, null=False, blank=False, choices=STATUS
    )

    def __str__(self):
        if self.offerer_details.propertyprocess.property.address_line_2 == "":
            property_address = "%s, %s (%s)" % (
                self.offerer_details.propertyprocess.property.postcode,
                self.offerer_details.propertyprocess.property.address_line_1,
                self.offerer_details.full_name,
            )
        else:
            property_address = "%s, %s, %s (%s)" % (
                self.offerer_details.propertyprocess.property.postcode,
                self.offerer_details.propertyprocess.property.address_line_1,
                self.offerer_details.propertyprocess.property.address_line_2,
                self.offerer_details.full_name,
            )
        return property_address


class Deal(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "date",
        ]
        verbose_name = "Deal"
        verbose_name_plural = "Deals"

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="deal",
    )
    date = models.DateField(null=False, blank=False)
    target_move_date = models.DateField()
    offer_accepted = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="offer_accepted"
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


class ExchangeMove(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Exchange & Move"
        verbose_name_plural = "Exchange & Move"

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="exchange_and_move",
    )
    exchange_date = models.DateField()
    completion_date = models.DateField()

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


class SalesProgression(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Sales Progression"
        verbose_name_plural = "Sales Progressions"

    TRUE_FALSE_CHOICES = ((True, "Done"), (False, "Not Done"))

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="sales_progression",
    )

    buyers_aml_checks_and_sales_memo = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    buyers_aml_checks_and_sales_memo_date = models.DateField(
        null=True, blank=True
    )

    buyers_initial_solicitors_paperwork = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    buyers_initial_solicitors_paperwork_date = models.DateField(
        null=True, blank=True
    )

    sellers_inital_solicitors_paperwork = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    sellers_inital_solicitors_paperwork_date = models.DateField(
        null=True, blank=True
    )

    draft_contracts_recieved_by_buyers_solicitors = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    draft_contracts_recieved_by_buyers_solicitors_date = models.DateField(
        null=True, blank=True
    )

    searches_paid_for = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    searches_paid_for_date = models.DateField(null=True, blank=True)

    searches_ordered = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    searches_ordered_date = models.DateField(null=True, blank=True)

    mortgage_application_submitted = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    mortgage_application_submitted_date = models.DateField(
        null=True, blank=True
    )

    mortgage_survey_arranged = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    mortgage_survey_arranged_date = models.DateField(null=True, blank=True)

    mortgage_survey_completed = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    mortgage_survey_completed_date = models.DateField(null=True, blank=True)

    all_search_results_recieved = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    all_search_results_recieved_date = models.DateField(null=True, blank=True)

    enquiries_raised = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    enquiries_raised_date = models.DateField(null=True, blank=True)

    structural_survey_booked = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    structural_survey_booked_date = models.DateField(null=True, blank=True)

    structural_survey_completed = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    structural_survey_completed_date = models.DateField(null=True, blank=True)

    enquiries_answered = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    enquiries_answered_date = models.DateField(null=True, blank=True)

    additional_enquiries_raised = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    additional_enquiries_raised_date = models.DateField(null=True, blank=True)

    all_enquiries_answered = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    all_enquiries_answered_date = models.DateField(null=True, blank=True)

    final_contracts_sent_out = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    final_contracts_sent_out_date = models.DateField(null=True, blank=True)

    buyers_final_contracts_signed = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    buyers_final_contracts_signed_date = models.DateField(
        null=True, blank=True
    )

    sellers_final_contracts_signed = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    sellers_final_contracts_signed_date = models.DateField(
        null=True, blank=True
    )

    buyers_deposit_sent = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    buyers_deposit_sent_date = models.DateField(null=True, blank=True)

    buyers_deposit_recieved = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    buyers_deposit_recieved_date = models.DateField(null=True, blank=True)

    completion_date_agreed = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    completion_date_agreed_date = models.DateField(null=True, blank=True)

    sales_notes = models.CharField(max_length=1000, null=True, blank=True)

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


class SalesProgressionSettings(UpdatedAndCreated):
    class Meta:
        ordering = [
            "sales_progression__propertyprocess__property__postcode",
            "sales_progression__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Sales Progression Settings"
        verbose_name_plural = "Sales Progressions Settings"

    SHOW_HIDE_CHOICES = ((True, "Show"), (False, "Hide"))

    sales_progression = models.OneToOneField(
        SalesProgression,
        on_delete=models.CASCADE,
        related_name="sales_progression_settings",
    )

    show_mortgage = models.BooleanField(
        null=True, blank=True, default=True, choices=SHOW_HIDE_CHOICES
    )

    show_survey = models.BooleanField(
        null=True, blank=True, default=True, choices=SHOW_HIDE_CHOICES
    )

    def __str__(self):
        if (
            self.sales_progression.propertyprocess.property.address_line_2
            == ""
        ):
            property_address = "%s, %s" % (
                self.sales_progression.propertyprocess.property.postcode,
                self.sales_progression.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.sales_progression.propertyprocess.property.postcode,
                self.sales_progression.propertyprocess.property.address_line_1,
                self.sales_progression.propertyprocess.property.address_line_2,
            )
        return property_address


class SalesProgressionPhase(UpdatedAndCreated):
    class Meta:
        ordering = [
            "sales_progression__propertyprocess__property__postcode",
            "sales_progression__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Sales Progression Phase"
        verbose_name_plural = "Sales Progressions Phase"

    PHASE_CHOICE = [
        (1, "Phase 1 Complete"),
        (2, "Phase 2 Complete"),
        (3, "Phase 3 Complete"),
        (4, "Phase 4 Complete"),
    ]

    sales_progression = models.OneToOneField(
        SalesProgression,
        on_delete=models.CASCADE,
        related_name="sales_progression_phase",
    )

    overall_phase = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        choices=PHASE_CHOICE,
    )

    phase_1 = models.BooleanField(default=False)

    phase_2 = models.BooleanField(default=False)

    phase_3 = models.BooleanField(default=False)

    phase_4 = models.BooleanField(default=False)

    def __str__(self):
        if (
            self.sales_progression.propertyprocess.property.address_line_2
            == ""
        ):
            property_address = "%s, %s" % (
                self.sales_progression.propertyprocess.property.postcode,
                self.sales_progression.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.sales_progression.propertyprocess.property.postcode,
                self.sales_progression.propertyprocess.property.address_line_1,
                self.sales_progression.propertyprocess.property.address_line_2,
            )
        return property_address


class PropertyChain(UpdatedAndCreated):
    class Meta:
        ordering = [
            "sales_progression__propertyprocess__property__postcode",
            "sales_progression__propertyprocess__property__address_line_1",
            "order",
        ]
        verbose_name = "Sales Progression Chain"
        verbose_name_plural = "Sales Progressions Chain"

    sales_progression = models.ForeignKey(
        SalesProgression,
        on_delete=models.CASCADE,
        related_name="sales_progression_chain",
    )
    company = models.CharField(max_length=150, null=False)
    branch = models.CharField(max_length=150, null=True)
    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False)
    postcode = models.CharField(max_length=8, null=True)
    chain_notes = models.CharField(max_length=1000, null=True, blank=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        if (
            self.sales_progression.propertyprocess.property.address_line_2
            == ""
        ):
            property_address = "%s, %s" % (
                self.sales_progression.propertyprocess.property.postcode,
                self.sales_progression.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.sales_progression.propertyprocess.property.postcode,
                self.sales_progression.propertyprocess.property.address_line_1,
                self.sales_progression.propertyprocess.property.address_line_2,
            )
        return property_address


class Marketing(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Marketing"
        verbose_name_plural = "Marketing"

    PREVIOUSCLIENT = "previous_client"
    APPLICANT = "applicant"
    SOCIALMEDIA = "social_media"
    RECOMMENDATION = "recommendation"
    LAURELS = "laurels_team_member_friends_or_family_of_laurels"
    FLYER = "sold_let_flyer"
    TOUT = "tout_letter"
    LETTER = "specific_letter"
    BROCHURE = "brochure"
    BUSINESSCARD = "business_card_drop"
    COMBINEDTOUTING = "combined_touting"
    GOOGLE = "google_search"
    MARKETING = "marketing_boards"
    LOCAL = "local_presence"
    SOLDONROAD = "sold_on_road"

    RIGHTMOVE = "rightmove"
    ZOOPLA = "zoopla"
    SOCIAL = "social_media"
    LAURELSWEBSITE = "laurels_website_search"
    LAURELSTEAM = "laurels_team_recommended"
    MARKETINGBOARDS = "marketing_boards"
    PUBLIC = "public_word_of_mouth"

    LAURELSASKED = "laurels_pro-actively_asked"
    SOCIALMEDIAMESSAGE = "social_media_message"
    PHONECALL = "phone_call_to_office"
    WEBSITE = "website_message"
    DIRECTEMAIL = "direct_email"

    HEAR_ABOUT_LAURELS = [
        (PREVIOUSCLIENT, "Previous Client"),
        (APPLICANT, "Applicant"),
        (SOCIALMEDIA, "Social Media Posts"),
        (RECOMMENDATION, "Recommendation"),
        (LAURELS, "Laurels Team Member/Friends or Family of Laurels"),
        (FLYER, "Sold/Let Flyer"),
        (TOUT, "Tout Letter"),
        (LETTER, "Specific Letter"),
        (BROCHURE, "Brochure Drop"),
        (BUSINESSCARD, "Business Card Drop"),
        (COMBINEDTOUTING, "Combined Touting"),
        (GOOGLE, "Google Search"),
        (MARKETING, "Marketing Boards"),
        (LOCAL, "Local Presence"),
        (SOLDONROAD, "Sold on Road"),
    ]

    APPLICANT_INTRO = [
        (RIGHTMOVE, "Rightmove"),
        (ZOOPLA, "Zoopla"),
        (SOCIAL, "Social Media"),
        (LAURELSWEBSITE, "Laurels Website Search"),
        (LAURELSTEAM, "Laurels Team Recommended"),
        (MARKETINGBOARDS, "Marketing Boards"),
        (PUBLIC, "Public Word of Mouth"),
    ]

    CONTACT_LAURELS = [
        (LAURELSASKED, "Laurels Pro-actively Asked"),
        (SOCIALMEDIAMESSAGE, "Social Media Message"),
        (PHONECALL, "Phone Call To Office"),
        (WEBSITE, "Website Message"),
        (DIRECTEMAIL, "Direct Email"),
    ]

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="marketing",
    )
    hear_about_laurels = models.CharField(
        max_length=100, null=True, blank=False, choices=HEAR_ABOUT_LAURELS
    )
    applicant_intro = models.CharField(
        max_length=100, null=True, blank=False, choices=APPLICANT_INTRO
    )
    contact_laurels = models.CharField(
        max_length=100, null=True, blank=False, choices=CONTACT_LAURELS
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


class PropertyFees(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Property Fee"
        verbose_name_plural = "Property Fees"

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="property_fees",
    )
    fee = models.DecimalField(
        decimal_places=2, max_digits=5, null=True, blank=True
    )
    price = models.IntegerField(null=True, blank=True)
    deal_date = models.DateField(null=True, blank=True)
    new_business = models.FloatField(null=True, blank=True)
    deal = models.BooleanField(default=False, null=True, blank=False)
    show_all = models.BooleanField(default=True, null=True, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)

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


@receiver(pre_save, sender=PropertyFees)
def save_field(sender, instance, **kwargs):
    if True:
        if instance.propertyprocess.sector == "sales":
            instance.calculated_value = instance.price * (
                instance.fee / 100
            )
        else:
            instance.calculated_value = (
                instance.price * (instance.fee / 100)
            ) * 12
