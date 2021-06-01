# Generated by Django 3.2 on 2021-05-25 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0007_propertyhistory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertyhistory",
            name="type",
            field=models.CharField(
                choices=[
                    ("property_event", "Property Event"),
                    ("offer", "Offer"),
                    ("progression", "Progression"),
                    ("management", "Management"),
                    ("other", "Other"),
                ],
                max_length=40,
            ),
        ),
        migrations.AlterField(
            model_name="propertyprocess",
            name="property",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="property",
                to="properties.property",
            ),
        ),
    ]