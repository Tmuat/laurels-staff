# Generated by Django 3.2.4 on 2021-09-09 14:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0096_auto_20210908_1626"),
    ]

    operations = [
        migrations.CreateModel(
            name="LettingsLandlordOrLaurelsInformation",
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
                (
                    "eicr_choice",
                    models.CharField(
                        choices=[
                            ("laurels", "Laurels"),
                            ("landlord", "Landlord"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "eicr_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "eicr_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "eicr_email",
                    models.EmailField(blank=True, max_length=100, null=True),
                ),
                ("eicr_expected_completion", models.DateField(null=True)),
                (
                    "epc_choice",
                    models.CharField(
                        choices=[
                            ("laurels", "Laurels"),
                            ("landlord", "Landlord"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "epc_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "epc_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "epc_email",
                    models.EmailField(blank=True, max_length=100, null=True),
                ),
                ("epc_expected_completion", models.DateField(null=True)),
                (
                    "gsc_choice",
                    models.CharField(
                        choices=[
                            ("laurels", "Laurels"),
                            ("landlord", "Landlord"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "gsc_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "gsc_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "gsc_email",
                    models.EmailField(blank=True, max_length=100, null=True),
                ),
                ("gsc_expected_completion", models.DateField(null=True)),
                (
                    "inventory_choice",
                    models.CharField(
                        choices=[
                            ("laurels", "Laurels"),
                            ("landlord", "Landlord"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "inventory_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "inventory_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "inventory_email",
                    models.EmailField(blank=True, max_length=100, null=True),
                ),
                ("inventory_expected_completion", models.DateField(null=True)),
                (
                    "professional_clean_choice",
                    models.CharField(
                        choices=[
                            ("laurels", "Laurels"),
                            ("landlord", "Landlord"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "professional_clean_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "professional_clean_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "professional_clean_email",
                    models.EmailField(blank=True, max_length=100, null=True),
                ),
                (
                    "professional_clean_expected_completion",
                    models.DateField(null=True),
                ),
                (
                    "propertyprocess",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="landlord_or_laurels",
                        to="properties.propertyprocess",
                    ),
                ),
            ],
            options={
                "verbose_name": "Selling Information",
                "verbose_name_plural": "Selling Information",
                "ordering": [
                    "propertyprocess__property__postcode",
                    "propertyprocess__property__address_line_1",
                ],
            },
        ),
    ]
