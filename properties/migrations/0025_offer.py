# Generated by Django 3.2 on 2021-05-27 09:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0024_offerercash"),
    ]

    operations = [
        migrations.CreateModel(
            name="Offer",
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
                ("date", models.DateField()),
                (
                    "offer",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("getting_verified", "Getting Verified"),
                            ("negotiating", "Negotiating"),
                            ("rejected", "Rejected"),
                            ("accepted", "Accepted"),
                            ("withdrawn", "Withdrawn"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "offerer_details",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offerdetails",
                        to="properties.offererdetails",
                    ),
                ),
            ],
            options={
                "verbose_name": "Offer Details",
                "verbose_name_plural": "Offer Details",
                "ordering": [
                    "offerer_details__propertyprocess__property__postcode",
                    "offerer_details__propertyprocess__property__address_line_1",
                    "offerer_details__full_name",
                    "date",
                ],
            },
        ),
    ]
