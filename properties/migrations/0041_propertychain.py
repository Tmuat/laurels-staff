# Generated by Django 3.2 on 2021-06-03 10:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0040_alter_salesprogressionphase_overall_phase"),
    ]

    operations = [
        migrations.CreateModel(
            name="PropertyChain",
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
                ("company", models.CharField(max_length=150)),
                ("branch", models.CharField(max_length=150, null=True)),
                ("address_line_1", models.CharField(max_length=150)),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                ("town", models.CharField(max_length=100)),
                ("postcode", models.CharField(max_length=8, null=True)),
                (
                    "chain_notes",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("order", models.IntegerField(null=True)),
                (
                    "sales_progression",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales_progression_chain",
                        to="properties.salesprogression",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sales Progression Chain",
                "verbose_name_plural": "Sales Progressions Chain",
                "ordering": [
                    "sales_progression__propertyprocess__property__postcode",
                    "sales_progression__propertyprocess__property__address_line_1",
                    "order",
                ],
            },
        ),
    ]
