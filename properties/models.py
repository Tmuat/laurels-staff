from datetime import date
import humanize

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.http import HttpResponse
from django.template.loader import render_to_string

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
    number_of_bedrooms = models.IntegerField(
        null=False, choices=NUMBER_BEDROOMS
    )
    tenure = models.CharField(
        max_length=50, null=True, blank=False, choices=TENURE
    )
    floor_space = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=False
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


class PropertyProcess(UpdatedAndCreated):
    class Meta:
        ordering = ["property__postcode", "property__address_line_1"]
        verbose_name = "Property Link"
        verbose_name_plural = "Property Links"

    LETTINGS = "lettings"
    SALES = "sales"

    ARCHIVED = -1
    WITHDRAWN = 0
    AWAITINGVALUATION = 1
    VALUATION = 2
    INSTRUCTION = 3
    DEAL = 4
    COMPLETE = 5

    SECTOR = [
        (LETTINGS, "Lettings"),
        (SALES, "Sales"),
    ]

    STATUS = [
        (ARCHIVED, "Archived"),
        (WITHDRAWN, "Withdrawn"),
        (AWAITINGVALUATION, "Awaiting Valuation"),
        (VALUATION, "Valuation Complete"),
        (INSTRUCTION, "Instructed - On The Market"),
        (DEAL, "Deal"),
        (COMPLETE, "Complete"),
    ]

    LEGACY = [(True, "Legacy"), (False, "Not Legacy")]

    sector = models.CharField(max_length=40, null=False, choices=SECTOR)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="property"
    )
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    macro_status = models.IntegerField(null=False, choices=STATUS)
    furthest_status = models.IntegerField(null=False, choices=STATUS)
    hub = models.ForeignKey(
        Hub, on_delete=models.CASCADE, null=False, blank=False
    )
    legacy_property = models.BooleanField(default=False, choices=LEGACY)
    previously_fallen_through = models.BooleanField(default=False)

    def __str__(self):
        if (
            self.property.address_line_2 == ""
            or self.property.address_line_2 is None
        ):
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

    def send_withdrawn_mail(self, request, reason, **kwargs):
        no_reply_email = settings.NO_REPLY_EMAIL
        admin_email = settings.ADMIN_EMAIL
        address = str(self.__str__())
        context = kwargs
        context.update(
            {
                "withdrawn": reason,
                "address": address,
                "hub": self.hub,
                "employee": self.employee,
            }
        )
        subject = f"Withdrawal: {address}"
        body = render_to_string("properties/emails/withdrawal.txt", context)

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=f'"Laurels Auto Emails" <{no_reply_email}>',
                recipient_list=[
                    admin_email,
                ],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

    def send_back_on_market_mail(self, request, **kwargs):
        no_reply_email = settings.NO_REPLY_EMAIL
        admin_email = settings.ADMIN_EMAIL
        address = str(self.__str__())
        context = kwargs
        context.update(
            {
                "marketing_board": self.instruction.marketing_board,
                "address": address,
                "hub": self.hub,
                "employee": self.employee,
            }
        )
        subject = f"Back On The Market: {address}"
        body = render_to_string(
            "properties/emails/back_on_market.txt", context
        )

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=f'"Laurels Auto Emails" <{no_reply_email}>',
                recipient_list=[
                    admin_email,
                ],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")


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
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 == None
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
    active = models.BooleanField(default=True)

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
    active = models.BooleanField(default=True)

    def send_mail(self, request, **kwargs):
        no_reply_email = settings.NO_REPLY_EMAIL
        admin_email = settings.ADMIN_EMAIL

        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 is None
        ):
            address = "%s, %s" % (
                self.propertyprocess.property.postcode,
                self.propertyprocess.property.address_line_1,
            )
        else:
            address = "%s, %s, %s" % (
                self.propertyprocess.property.postcode,
                self.propertyprocess.property.address_line_1,
                self.propertyprocess.property.address_line_2,
            )

        context = kwargs
        context.update(
            {
                "marketing_board": self.marketing_board,
                "address": address,
                "hub": self.propertyprocess.hub,
                "employee": self.propertyprocess.employee,
            }
        )
        if self.propertyprocess.sector == PropertyProcess.SALES:
            subject = f"Sales Instruction: {address}"
        else:
            subject = f"Lettings Instruction: {address}"
        body = render_to_string(
            "properties/emails/new_instruction.txt", context
        )

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=f'"Laurels Auto Emails" <{no_reply_email}>',
                recipient_list=[
                    admin_email,
                ],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

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


class InstructionChange(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Instruction Change"
        verbose_name_plural = "Instruction Changes"

    WEEKS16 = 16
    WEEKS12 = 12
    WEEKS10 = 10
    WEEKS8 = 8
    WEEKS6 = 6
    WEEKS4 = 4

    AGREEMENT_TYPE = [
        (Instruction.MULTI, "Multi"),
        (Instruction.SOLE, "Sole"),
    ]

    LENGTH_OF_CONTRACT = [
        (WEEKS16, "16 Weeks"),
        (WEEKS12, "12 Weeks"),
        (WEEKS10, "10 Weeks"),
        (WEEKS8, "8 Weeks"),
        (WEEKS6, "6 Weeks"),
        (WEEKS4, "4 Weeks (Multi Only)"),
    ]

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="instruction_change",
    )
    agreement_type_bool = models.BooleanField(default=False)
    agreement_type = models.CharField(max_length=15, choices=AGREEMENT_TYPE)
    fee_agreed_bool = models.BooleanField(default=False)
    fee_agreed = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=False
    )
    length_of_contract_bool = models.BooleanField(default=False)
    length_of_contract = models.IntegerField(
        null=True, blank=False, choices=LENGTH_OF_CONTRACT
    )

    def __str__(self):
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 == None
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

    SERVICE_LEVEL = [
        (INTRO, "Intro Only"),
        (RENTCOLLECT, "Rent Collect"),
        (FULLYMANAGED, "Fully Managed"),
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

    UNDER_OFFER = "under_offer"
    NO_CHAIN = "no_chain"
    LET_TO_BUY = "let_to_buy"
    NOT_ON_MARKET = "not_on_market"

    FUNDING = [(CASH, "Cash"), (MORTGAGE, "Mortgage")]

    STATUS = [
        (UNDER_OFFER, "Under Offer"),
        (NO_CHAIN, "No Chain"),
        (LET_TO_BUY, "Let To Buy"),
        (NOT_ON_MARKET, "Not On Market"),
    ]

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="offerer_details",
    )
    full_name = models.CharField(max_length=100, null=False, blank=False)
    completed_offer_form = models.BooleanField(
        default=False, null=True, blank=True
    )
    funding = models.CharField(
        max_length=10, null=True, blank=False, choices=FUNDING
    )
    status = models.CharField(
        max_length=20, null=True, blank=False, choices=STATUS
    )

    @property
    def calculate_str_length(self, **kwargs):
        return len(self.full_name)

    def __str__(self):
        return self.full_name


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
        if (
            self.offerer_details.propertyprocess.property.address_line_2 == ""
            or self.offerer_details.propertyprocess.property.address_line_2
            == None
        ):
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
        if (
            self.offerer_details.propertyprocess.property.address_line_2 == ""
            or self.offerer_details.propertyprocess.property.address_line_2
            == None
        ):
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


class OffererDetailsLettings(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "full_name",
        ]
        verbose_name = "Offerer History Lettings"
        verbose_name_plural = "Offerer History Lettings"

    COMPLETED = [(True, "Completed"), (False, "Incomplete")]

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="offerer_details_lettings",
    )
    full_name = models.CharField(max_length=100, null=False, blank=False)
    completed_offer_form = models.BooleanField(
        default=False, null=True, blank=False, choices=COMPLETED
    )

    @property
    def calculate_str_length(self, **kwargs):
        return len(self.full_name)

    def __str__(self):
        return self.full_name


class Offer(UpdatedAndCreated):
    class Meta:
        ordering = [
            "offerer_details__propertyprocess__property__postcode",
            "offerer_details__propertyprocess__property__address_line_1",
            "offerer_details__full_name",
            "-date",
            "-created",
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
        null=True,
        related_name="offerdetails",
    )
    offerer_lettings_details = models.ForeignKey(
        OffererDetailsLettings,
        on_delete=models.CASCADE,
        null=True,
        related_name="offerdetailslettings",
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

    @property
    def calculate_date(self, **kwargs):
        time_between_insertion = date.today() - self.date
        return time_between_insertion

    def __str__(self):
        if self.offerer_details:
            str = "%s (£%s)" % (
                self.offerer_details.full_name,
                humanize.intcomma(self.offer),
            )
        elif self.offerer_lettings_details:
            str = "%s (£%s)" % (
                self.offerer_lettings_details.full_name,
                humanize.intcomma(self.offer),
            )
        return str


class OfferLettingsExtra(UpdatedAndCreated):
    class Meta:
        ordering = [
            "offer_extra__offerer_lettings_details__propertyprocess__property__postcode",
            "offer_extra__offerer_lettings_details__propertyprocess__property__address_line_1",
            "offer_extra__offerer_lettings_details__full_name",
            "-offer_extra__date",
            "-created",
        ]
        verbose_name = "Offer Extra"
        verbose_name_plural = "Offer Extra"

    SIX = 6
    TWELVE = 12
    EIGHTEEN = 18
    TWENTYFOUR = 24

    TERM = [
        (SIX, "6 Months"),
        (TWELVE, "12 Months"),
        (EIGHTEEN, "18 Months"),
        (TWENTYFOUR, "24 Months"),
    ]

    offer_extra = models.OneToOneField(
        Offer,
        on_delete=models.CASCADE,
        related_name="offer_extra",
    )
    proposed_move_in_date = models.DateField(null=True, blank=False)
    term = models.IntegerField(null=True, blank=False, choices=TERM)

    def __str__(self):
        return "%s (£%s)" % (
            self.offer_extra.offerer_details.full_name,
            humanize.intcomma(self.offer),
        )


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
    offer_accepted = models.OneToOneField(
        Offer, on_delete=models.CASCADE, related_name="offer_accepted"
    )

    def send_deal_mail(self, request, marketing_board, **kwargs):
        no_reply_email = settings.NO_REPLY_EMAIL
        admin_email = settings.ADMIN_EMAIL
        humanized_offer = humanize.intcomma(self.offer_accepted.offer)
        address = str(self.__str__)
        context = kwargs
        context.update(
            {
                "marketing_board": marketing_board,
                "address": address,
                "hub": self.propertyprocess.hub,
                "employee": self.propertyprocess.employee,
                "offer": self.offer_accepted,
                "humanized_offer": humanized_offer,
            }
        )
        subject = f"Sales Deal: {address}"
        body = render_to_string("properties/emails/new_deal.txt", context)

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=f'"Laurels Auto Emails" <{no_reply_email}>',
                recipient_list=[
                    admin_email,
                ],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

    def send_lettings_deal_mail(self, request, marketing_board, **kwargs):
        no_reply_email = settings.NO_REPLY_EMAIL
        admin_email = settings.ADMIN_EMAIL
        humanized_offer = humanize.intcomma(self.offer_accepted.offer)
        address = str(self.__str__)
        context = kwargs
        context.update(
            {
                "marketing_board": marketing_board,
                "address": address,
                "hub": self.propertyprocess.hub,
                "employee": self.propertyprocess.employee,
                "offer": self.offer_accepted,
                "humanized_offer": humanized_offer,
            }
        )
        subject = f"Sales Deal: {address}"
        body = render_to_string(
            "properties/emails/new_lettings_deal.txt", context
        )

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=f'"Laurels Auto Emails" <{no_reply_email}>',
                recipient_list=[
                    admin_email,
                ],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

    def __str__(self):
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 == None
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


class DealExtraLettings(UpdatedAndCreated):
    class Meta:
        ordering = [
            "deal__propertyprocess__property__postcode",
            "deal__propertyprocess__property__address_line_1",
            "deal__date",
        ]
        verbose_name = "Deal Extra"
        verbose_name_plural = "Deal Extra"

    NONE = 0
    SIX = 6
    TWELVE = 12
    EIGHTEEN = 18
    TWENTYFOUR = 24
    THIRTYSIX = 36

    TERM = [
        (SIX, "6 Months"),
        (TWELVE, "12 Months"),
        (EIGHTEEN, "18 Months"),
        (TWENTYFOUR, "24 Months"),
        (THIRTYSIX, "36 Months"),
    ]

    BREAKCLAUSE = [
        (NONE, "No Break Clause"),
        (SIX, "6 Months"),
        (TWELVE, "12 Months"),
        (EIGHTEEN, "18 Months"),
        (TWENTYFOUR, "24 Months"),
    ]

    deal = models.OneToOneField(
        Deal,
        on_delete=models.CASCADE,
        related_name="deal_extra",
    )
    term = models.IntegerField(null=True, blank=False, choices=TERM)
    break_clause = models.IntegerField(
        null=True, blank=False, choices=BREAKCLAUSE
    )


class ExchangeMove(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Exchange & Move"
        verbose_name_plural = "Exchange & Move"

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="exchange_and_move",
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


class ExchangeMoveSales(UpdatedAndCreated):
    class Meta:
        ordering = [
            "exchange__propertyprocess__property__postcode",
            "exchange__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Exchange & Move Sales"
        verbose_name_plural = "Exchange & Move Sales"

    exchange = models.OneToOneField(
        ExchangeMove,
        on_delete=models.CASCADE,
        related_name="exchange_and_move_sales",
    )
    exchange_date = models.DateField()
    completion_date = models.DateField()

    def send_exchange_mail(self, request, **kwargs):
        no_reply_email = settings.NO_REPLY_EMAIL
        admin_email = settings.ADMIN_EMAIL
        address = str(self.__str__())
        context = kwargs
        context.update(
            {
                "address": address,
                "hub": self.exchange.propertyprocess.hub,
                "employee": self.exchange.propertyprocess.employee,
                "exchange": self.exchange_date.strftime("%d/%m/%Y"),
                "completion": self.completion_date.strftime("%d/%m/%Y"),
            }
        )
        subject = f"Exchange: {address}"
        body = render_to_string("properties/emails/exchange.txt", context)

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=f'"Laurels Auto Emails" <{no_reply_email}>',
                recipient_list=[
                    admin_email,
                ],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

    def __str__(self):
        if (
            self.exchange.propertyprocess.property.address_line_2 == ""
            or self.exchange.propertyprocess.property.address_line_2 is None
        ):
            property_address = "%s, %s" % (
                self.exchange.propertyprocess.property.postcode,
                self.exchange.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.exchange.propertyprocess.property.postcode,
                self.exchange.propertyprocess.property.address_line_1,
                self.exchange.propertyprocess.property.address_line_2,
            )
        return property_address


class ExchangeMoveLettings(UpdatedAndCreated):
    class Meta:
        ordering = [
            "exchange__propertyprocess__property__postcode",
            "exchange__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Exchange & Move Lettings"
        verbose_name_plural = "Exchange & Move Lettings"

    exchange = models.OneToOneField(
        ExchangeMove,
        on_delete=models.CASCADE,
        related_name="exchange_and_move_lettings",
    )
    move_in_date = models.DateField()
    first_renewal = models.DateField()

    def send_exchange_mail(self, request, **kwargs):
        no_reply_email = settings.NO_REPLY_EMAIL
        admin_email = settings.ADMIN_EMAIL
        address = str(self.exchange.propertyprocess.__str__)
        context = kwargs
        context.update(
            {
                "address": address,
                "hub": self.exchange.propertyprocess.hub,
                "employee": self.exchange.propertyprocess.employee,
                "move_in_date": self.move_in_date.strftime("%d/%m/%Y"),
                "first_renewal": self.first_renewal.strftime("%d/%m/%Y"),
            }
        )
        subject = f"Lettings Exchange: {address}"
        body = render_to_string(
            "properties/emails/exchange_lettings.txt", context
        )

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=f'"Laurels Auto Emails" <{no_reply_email}>',
                recipient_list=[
                    admin_email,
                ],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

    def __str__(self):
        if (
            self.exchange.propertyprocess.property.address_line_2 == ""
            or self.exchange.propertyprocess.property.address_line_2 is None
        ):
            property_address = "%s, %s" % (
                self.exchange.propertyprocess.property.postcode,
                self.exchange.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.exchange.propertyprocess.property.postcode,
                self.exchange.propertyprocess.property.address_line_1,
                self.exchange.propertyprocess.property.address_line_2,
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

    primary_progressor = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
        related_name="sales_progressor",
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

    mortgage_offer_with_solicitors = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    mortgage_offer_with_solicitors_date = models.DateField(
        null=True, blank=True
    )

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
            or self.sales_progression.propertyprocess.property.address_line_2
            == None
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
            or self.sales_progression.propertyprocess.property.address_line_2
            == None
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
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "order",
        ]
        verbose_name = "Sales Progression Chain"
        verbose_name_plural = "Sales Progressions Chain"

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="property_chain",
    )
    company = models.CharField(max_length=150, null=False)
    branch = models.CharField(max_length=150, null=True)
    address_line_1 = models.CharField(max_length=150, null=False)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=100, null=False)
    postcode = models.CharField(max_length=8, null=True)
    chain_notes = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True)

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
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 == None
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


class PropertyFees(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "-date",
            "-created",
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
    date = models.DateField(null=True, blank=True)
    new_business = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=False, null=True, blank=False)
    show_all = models.BooleanField(default=True, null=True, blank=False)

    def __str__(self):
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 == None
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


@receiver(pre_save, sender=PropertyFees)
def save_field(sender, instance, **kwargs):
    if True:
        if instance.propertyprocess.sector == "sales":
            new_business = round(instance.price * (instance.fee / 100), 2)
            instance.new_business = new_business
        elif instance.propertyprocess.sector == "lettings":
            new_business = round((instance.price * (instance.fee / 100)) * 12)
            instance.new_business = new_business


class ProgressionNotes(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "-created",
        ]
        verbose_name = "Progression Note"
        verbose_name_plural = "Progression Notes"

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="progression_notes",
    )
    notes = models.TextField(null=True, blank=True)

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


class PropertySellingInformation(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Selling Information"
        verbose_name_plural = "Selling Information"

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="selling_information",
    )
    seller_name = models.CharField(max_length=100, null=True, blank=True)
    seller_phone = models.CharField(max_length=15, null=True, blank=True)
    seller_email = models.EmailField(max_length=100, null=True, blank=True)
    buyer_name = models.CharField(max_length=100, null=True, blank=True)
    buyer_phone = models.CharField(max_length=15, null=True, blank=True)
    buyer_email = models.EmailField(max_length=100, null=True, blank=True)
    seller_sol_name = models.CharField(max_length=100, null=True, blank=True)
    seller_sol_firm = models.CharField(max_length=100, null=True, blank=True)
    seller_sol_phone = models.CharField(max_length=15, null=True, blank=True)
    seller_sol_email = models.EmailField(max_length=100, null=True, blank=True)
    buyer_sol_name = models.CharField(max_length=100, null=True, blank=True)
    buyer_sol_firm = models.CharField(max_length=100, null=True, blank=True)
    buyer_sol_phone = models.CharField(max_length=15, null=True, blank=True)
    buyer_sol_email = models.EmailField(max_length=100, null=True, blank=True)
    broker_name = models.CharField(max_length=100, null=True, blank=True)
    broker_firm = models.CharField(max_length=100, null=True, blank=True)
    broker_phone = models.CharField(max_length=15, null=True, blank=True)
    broker_email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 == None
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


class Reduction(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
            "-created",
        ]
        verbose_name = "Reduction"
        verbose_name_plural = "Reductions"

    propertyprocess = models.ForeignKey(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="reduction",
    )
    date = models.DateField(null=False, blank=False)
    price_change = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        if (
            self.propertyprocess.property.address_line_2 == ""
            or self.propertyprocess.property.address_line_2 == None
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


class LettingsProgression(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Lettings Progression"
        verbose_name_plural = "Lettings Progressions"

    TRUE_FALSE_CHOICES = ((True, "Done"), (False, "Not Done"))

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="lettings_progression",
    )

    primary_progressor = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
        related_name="lettings_progressor",
    )

    contact_touch_point_to_ll_and_tt = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    contact_touch_point_to_ll_and_tt_date = models.DateField(
        null=True, blank=True
    )

    reference_forms_sent_to_tenant = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    reference_forms_sent_to_tenant_date = models.DateField(
        null=True, blank=True
    )

    compliance_form_sent_to_landlord = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    compliance_form_sent_to_landlord_date = models.DateField(
        null=True, blank=True
    )

    google_drive_and_email_inbox = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    google_drive_and_email_inbox_date = models.DateField(null=True, blank=True)

    tenancy_created_on_expert_agent = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    tenancy_created_on_expert_agent_date = models.DateField(
        null=True, blank=True
    )

    references_passed = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    references_passed_date = models.DateField(null=True, blank=True)

    gas_safety_certificate = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    gas_safety_certificate_expiry = models.DateField(null=True, blank=True)
    gas_safety_certificate_date = models.DateField(null=True, blank=True)

    electrical_certificate = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    electrical_certificate_expiry = models.DateField(null=True, blank=True)
    electrical_certificate_date = models.DateField(null=True, blank=True)

    epc_certificate = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    epc_certificate_expiry = models.DateField(null=True, blank=True)
    epc_certificate_date = models.DateField(null=True, blank=True)

    tenancy_certificate_sent = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    tenancy_certificate_sent_date = models.DateField(null=True, blank=True)

    tenancy_agreement_signed = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    tenancy_agreement_signed_date = models.DateField(null=True, blank=True)

    tenant_invoice_sent = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    tenant_invoice_sent_date = models.DateField(null=True, blank=True)

    move_in_funds_received = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    move_in_funds_received_date = models.DateField(null=True, blank=True)

    prescribed_info_and_statutory_docs_sent = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    prescribed_info_and_statutory_docs_sent_date = models.DateField(
        null=True, blank=True
    )

    deposit_registered_with_tds = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    deposit_registered_with_tds_date = models.DateField(null=True, blank=True)

    landlord_invoices_sent_to_ea = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    landlord_invoices_sent_to_ea_date = models.DateField(null=True, blank=True)

    right_to_rent = models.BooleanField(
        null=True, blank=True, default=False, choices=TRUE_FALSE_CHOICES
    )
    right_to_rent_date = models.DateField(null=True, blank=True)

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


class LettingsProgressionSettings(UpdatedAndCreated):
    class Meta:
        ordering = [
            "lettings_progression__propertyprocess__property__postcode",
            "lettings_progression__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Lettings Progression Settings"
        verbose_name_plural = "Lettings Progressions Settings"

    SHOW_HIDE_CHOICES = ((True, "Show"), (False, "Hide"))

    lettings_progression = models.OneToOneField(
        LettingsProgression,
        on_delete=models.CASCADE,
        related_name="lettings_progression_settings",
    )

    show_gas = models.BooleanField(
        null=True, blank=True, default=True, choices=SHOW_HIDE_CHOICES
    )

    def __str__(self):
        if (
            self.lettings_progression.propertyprocess.property.address_line_2
            == ""
            or self.lettings_progression.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.lettings_progression.propertyprocess.property.postcode,
                self.lettings_progression.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.lettings_progression.propertyprocess.property.postcode,
                self.lettings_progression.propertyprocess.property.address_line_1,
                self.lettings_progression.propertyprocess.property.address_line_2,
            )
        return property_address


class LettingsProgressionPhase(UpdatedAndCreated):
    class Meta:
        ordering = [
            "lettings_progression__propertyprocess__property__postcode",
            "lettings_progression__propertyprocess__property__address_line_1",
        ]
        verbose_name = "Lettings Progression Phase"
        verbose_name_plural = "Lettings Progressions Phase"

    PHASE_CHOICE = [
        (1, "Phase 1 Complete"),
        (2, "Phase 2 Complete"),
        (3, "Phase 3 Complete"),
        (4, "Phase 4 Complete"),
    ]

    lettings_progression = models.OneToOneField(
        LettingsProgression,
        on_delete=models.CASCADE,
        related_name="lettings_progression_phase",
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
            self.lettings_progression.propertyprocess.property.address_line_2
            == ""
            or self.lettings_progression.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.lettings_progression.propertyprocess.property.postcode,
                self.lettings_progression.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.lettings_progression.propertyprocess.property.postcode,
                self.lettings_progression.propertyprocess.property.address_line_1,
                self.lettings_progression.propertyprocess.property.address_line_2,
            )
        return property_address


class LettingsLandlordOrLaurelsInformation(UpdatedAndCreated):
    class Meta:
        ordering = [
            "propertyprocess__property__postcode",
            "propertyprocess__property__address_line_1",
        ]
        verbose_name = "Selling Information"
        verbose_name_plural = "Selling Information"

    LAURELS = "laurels"
    LANDLORD = "landlord"

    CHOICE = [
        (LAURELS, "Laurels"),
        (LANDLORD, "Landlord"),
    ]

    propertyprocess = models.OneToOneField(
        PropertyProcess,
        on_delete=models.CASCADE,
        related_name="landlord_or_laurels",
    )

    eicr_choice = models.CharField(
        max_length=10, null=True, blank=False, choices=CHOICE
    )
    eicr_name = models.CharField(max_length=100, null=True, blank=True)
    eicr_phone = models.CharField(max_length=15, null=True, blank=True)
    eicr_email = models.EmailField(max_length=100, null=True, blank=True)
    eicr_expected_completion = models.DateField(null=True, blank=False)

    epc_choice = models.CharField(
        max_length=10, null=True, blank=False, choices=CHOICE
    )
    epc_name = models.CharField(max_length=100, null=True, blank=True)
    epc_phone = models.CharField(max_length=15, null=True, blank=True)
    epc_email = models.EmailField(max_length=100, null=True, blank=True)
    epc_expected_completion = models.DateField(null=True, blank=False)

    gsc_choice = models.CharField(
        max_length=10, null=True, blank=False, choices=CHOICE
    )
    gsc_name = models.CharField(max_length=100, null=True, blank=True)
    gsc_phone = models.CharField(max_length=15, null=True, blank=True)
    gsc_email = models.EmailField(max_length=100, null=True, blank=True)
    gsc_expected_completion = models.DateField(null=True, blank=False)

    inventory_choice = models.CharField(
        max_length=10, null=True, blank=False, choices=CHOICE
    )
    inventory_name = models.CharField(max_length=100, null=True, blank=True)
    inventory_phone = models.CharField(max_length=15, null=True, blank=True)
    inventory_email = models.EmailField(max_length=100, null=True, blank=True)
    inventory_expected_completion = models.DateField(null=True, blank=False)

    professional_clean_choice = models.CharField(
        max_length=10, null=True, blank=False, choices=CHOICE
    )
    professional_clean_name = models.CharField(
        max_length=100, null=True, blank=True
    )
    professional_clean_phone = models.CharField(
        max_length=15, null=True, blank=True
    )
    professional_clean_email = models.EmailField(
        max_length=100, null=True, blank=True
    )
    professional_clean_expected_completion = models.DateField(
        null=True, blank=False
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
