# Generated by Django 3.2.4 on 2021-08-04 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0080_offerlettingsextra"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="offerlettingsextra",
            options={
                "ordering": [
                    "offer_extra__offerer_lettings_details__propertyprocess__property__postcode",
                    "offer_extra__offerer_lettings_details__propertyprocess__property__address_line_1",
                    "offer_extra__offerer_lettings_details__full_name",
                    "-offer_extra__date",
                    "-created",
                ],
                "verbose_name": "Offer Extra",
                "verbose_name_plural": "Offer Extra",
            },
        ),
        migrations.AddField(
            model_name="offer",
            name="offerer_lettings_details",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offerdetailslettings",
                to="properties.offererdetailslettings",
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="offerer_details",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offerdetails",
                to="properties.offererdetails",
            ),
        ),
    ]
