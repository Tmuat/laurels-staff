# Generated by Django 3.2.4 on 2021-08-11 13:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("lettings", "0004_auto_20210811_1139"),
    ]

    operations = [
        migrations.CreateModel(
            name="Electrical",
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
                ("expiry", models.DateField()),
                (
                    "lettings_properties",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="electrical",
                        to="lettings.lettingproperties",
                    ),
                ),
            ],
            options={
                "verbose_name": "Electrical",
                "verbose_name_plural": "Electrical",
                "ordering": [
                    "-date",
                    "lettings_properties__propertyprocess__property__postcode",
                    "lettings_properties__propertyprocess__property__address_line_1",
                ],
            },
        ),
    ]
