# Generated by Django 3.2.4 on 2021-08-06 11:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0084_auto_20210806_1244"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeMoveLettings",
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
                ("move_in_date", models.DateField()),
                ("first_renewal", models.DateField()),
                (
                    "exchange",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchange_and_move_lettings",
                        to="properties.exchangemove",
                    ),
                ),
            ],
            options={
                "verbose_name": "Exchange & Move Lettings",
                "verbose_name_plural": "Exchange & Move Lettings",
                "ordering": [
                    "exchange__propertyprocess__property__postcode",
                    "exchange__propertyprocess__property__address_line_1",
                ],
            },
        ),
    ]
