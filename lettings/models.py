from django.db import models

from common.models import UpdatedAndCreated
from properties.models import PropertyProcess, InstructionLettingsExtra
from users.models import Profile


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


class Maintenance(UpdatedAndCreated):
    class Meta:
        ordering = [
            "lettings_properties__propertyprocess__property__postcode",
            "lettings_properties__propertyprocess__property__address_line_1",
            "-target_start_date"
        ]
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenance"

    NEW = "new"
    AWAITING_CONTRACTOR = "awaiting_contractor"
    AWAITING_LANDLORD = "awaiting_landlord"
    AWAITING_TENANT = "awaiting_tenant"
    WAITING_CONTRACTOR = "waiting_contractor"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FUTURE_JOB = "future_job"

    NO_CHARGE = "no_charge"
    CON_BILLS_TENANT = "con_bills_tenant"
    CON_BILLS_LANDLORD = "con_bills_landlord"
    CON_BILLS_US = "con_bills_us"

    STATUS = [
        (NEW, "New"),
        (AWAITING_CONTRACTOR, "Awaiting Contractor"),
        (AWAITING_LANDLORD, "Awaiting Landlord Consent"),
        (AWAITING_TENANT, "Awaiting Tenant Availability"),
        (WAITING_CONTRACTOR, "Waiting For Contractor"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (FUTURE_JOB, "Future Job"),
    ]

    BILLING = [
        (NO_CHARGE, "No Charge"),
        (CON_BILLS_TENANT, "Contractor Bills Tenant"),
        (CON_BILLS_LANDLORD, "Contractor Bills Landlord"),
        (CON_BILLS_US, "Contractor Bills Us"),
    ]

    PRIORITY = [
        (1, "Urgent"),
        (2, "High"),
        (3, "Medium"),
        (4, "Low")
    ]

    lettings_properties = models.ForeignKey(
        LettingProperties, on_delete=models.CASCADE, related_name="maintenance"
    )
    type = models.CharField(max_length=25, null=False, blank=False)
    status = models.CharField(
        max_length=25, null=False, blank=False, choices=STATUS
    )
    managed_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="managed_maintenance",
    )
    billing_status = models.CharField(
        max_length=30, null=False, blank=False, choices=BILLING
    )
    reported_by = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    priority = models.PositiveIntegerField(
        null=True, blank=False, choices=PRIORITY
    )
    target_start_date = models.DateField(
        null=True,
        blank=True,
    )
    actual_start_date = models.DateField(
        null=True,
        blank=True,
    )
    target_completion_date = models.DateField(
        null=True,
        blank=True,
    )
    actual_completion_date = models.DateField(
        null=True,
        blank=True,
    )
    summary = models.CharField(max_length=200, null=True, blank=True)
    cost = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    contractor = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )

    def __str__(self):
        if (
            self.lettings_properties.propertyprocess.property.address_line_2
            == ""
            or self.lettings_properties.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s (%s)" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
                self.type,
            )
        else:
            property_address = "%s, %s, %s (%s)" % (
                self.lettings_properties.propertyprocess.property.postcode,
                self.lettings_properties.propertyprocess.property.address_line_1,
                self.lettings_properties.propertyprocess.property.address_line_2,
                self.type,
            )
        return property_address


class MaintenanceNotes(UpdatedAndCreated):
    class Meta:
        ordering = [
            "maintenance__lettings_properties__propertyprocess__property__postcode",
            "maintenance__lettings_properties__propertyprocess__property__address_line_1",
            "-created",
        ]
        verbose_name = "Maintenance Note"
        verbose_name_plural = "Maintenance Notes"

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="maintenance_notes",
    )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        if (
            self.maintenance.lettings_properties.propertyprocess.property.address_line_2
            == ""
            or self.maintenance.lettings_properties.propertyprocess.property.address_line_2
            is None
        ):
            property_address = "%s, %s" % (
                self.maintenance.lettings_properties.propertyprocess.property.postcode,
                self.maintenance.lettings_properties.propertyprocess.property.address_line_1,
            )
        else:
            property_address = "%s, %s, %s" % (
                self.maintenance.lettings_properties.propertyprocess.property.postcode,
                self.maintenance.lettings_properties.propertyprocess.property.address_line_1,
                self.maintenance.lettings_properties.propertyprocess.property.address_line_2,
            )
        return property_address
