# Generated by Django 3.2 on 2021-06-02 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0037_alter_salesprogressionphase_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="salesprogression",
            options={
                "ordering": [
                    "propertyprocess__property__postcode",
                    "propertyprocess__property__address_line_1",
                ],
                "verbose_name": "Sales Progression",
                "verbose_name_plural": "Sales Progressions",
            },
        ),
        migrations.AlterModelOptions(
            name="salesprogressionsettings",
            options={
                "ordering": [
                    "sale_progression__propertyprocess__property__postcode",
                    "sale_progression__propertyprocess__property__address_line_1",
                ],
                "verbose_name": "Sales Progression Settings",
                "verbose_name_plural": "Sales Progressions Settings",
            },
        ),
    ]