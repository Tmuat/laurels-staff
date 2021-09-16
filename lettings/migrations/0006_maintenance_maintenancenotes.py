# Generated by Django 3.2.4 on 2021-09-10 10:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0015_remove_profile_office_comm"),
        ("lettings", "0005_electrical"),
    ]

    operations = [
        migrations.CreateModel(
            name="Maintenance",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created_by", models.CharField(blank=True, max_length=100)),
                ("updated_by", models.CharField(blank=True, max_length=100)),
                ("type", models.CharField(max_length=25)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("awaiting_contractor", "Awaiting Contractor"),
                            ("awaiting_landlord", "Awaiting Landlord Consent"),
                            (
                                "awaiting_tenant",
                                "Awaiting Tenant Availability",
                            ),
                            ("waiting_contractor", "Waiting For Contractor"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                            ("future_job", "Future Job"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "billing_status",
                    models.CharField(
                        choices=[
                            ("no_charge", "No Charge"),
                            ("con_bills_tenant", "Contractor Bills Tenant"),
                            (
                                "con_bills_landlord",
                                "Contractor Bills Landlord",
                            ),
                            ("con_bills_us", "Contractor Bills Us"),
                        ],
                        max_length=30,
                    ),
                ),
                ("reported_by", models.CharField(max_length=50)),
                ("target_start_date", models.DateField(blank=True, null=True)),
                ("actual_start_date", models.DateField(blank=True, null=True)),
                (
                    "target_completion_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "actual_completion_date",
                    models.DateField(blank=True, null=True),
                ),
                ("summary", models.TextField(blank=True, null=True)),
                ("details", models.TextField(blank=True, null=True)),
                ("contractor", models.CharField(max_length=80)),
                (
                    "lettings_properties",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintenance",
                        to="lettings.lettingproperties",
                    ),
                ),
                (
                    "managed_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="managed_maintenance",
                        to="users.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Maintenance",
                "verbose_name_plural": "Maintenance",
                "ordering": [
                    "lettings_properties__propertyprocess__property__postcode",
                    "lettings_properties__propertyprocess__property__address_line_1",
                ],
            },
        ),
        migrations.CreateModel(
            name="MaintenanceNotes",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created_by", models.CharField(blank=True, max_length=100)),
                ("updated_by", models.CharField(blank=True, max_length=100)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "maintenance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintenance_notes",
                        to="lettings.maintenance",
                    ),
                ),
            ],
            options={
                "verbose_name": "Maintenance Note",
                "verbose_name_plural": "Maintenance Notes",
                "ordering": [
                    "maintenance__lettings_properties__propertyprocess__property__postcode",
                    "maintenance__lettings_properties__propertyprocess__property__address_line_1",
                    "-created",
                ],
            },
        ),
    ]
