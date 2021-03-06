# Generated by Django 3.2 on 2021-06-01 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0029_offer_propertyprocess"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="propertyprocess",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deal",
                to="properties.propertyprocess",
            ),
        ),
    ]
