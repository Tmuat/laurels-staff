# Generated by Django 3.2 on 2021-06-15 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0056_propertyprocess_furthest_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="propertyfees",
            options={
                "ordering": [
                    "propertyprocess__property__postcode",
                    "propertyprocess__property__address_line_1",
                    "-date",
                ],
                "verbose_name": "Property Fee",
                "verbose_name_plural": "Property Fees",
            },
        ),
    ]
