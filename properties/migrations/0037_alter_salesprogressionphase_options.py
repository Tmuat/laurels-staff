# Generated by Django 3.2 on 2021-06-02 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0036_auto_20210602_1525"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="salesprogressionphase",
            options={
                "ordering": [
                    "sale_progression__propertyprocess__property__postcode",
                    "sale_progression__propertyprocess__property__address_line_1",
                ],
                "verbose_name": "Sales Progression Phase",
                "verbose_name_plural": "Sales Progressions Phase",
            },
        ),
    ]