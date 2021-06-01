# Generated by Django 3.2 on 2021-05-26 15:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0009_auto_20210526_1300"),
    ]

    operations = [
        migrations.CreateModel(
            name="OffererDetails",
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
                ("full_name", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("completed_offer_form", models.BooleanField(null=True)),
                (
                    "funding",
                    models.CharField(
                        choices=[("cash", "Cash"), ("mortgage", "Mortgage")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "propertyprocess",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offerer_details",
                        to="properties.propertyprocess",
                    ),
                ),
            ],
            options={
                "verbose_name": "Offerer Details",
                "verbose_name_plural": "Offerer Details",
                "ordering": [
                    "propertyprocess__property__postcode",
                    "propertyprocess__property__address_line_1",
                    "full_name",
                ],
            },
        ),
    ]