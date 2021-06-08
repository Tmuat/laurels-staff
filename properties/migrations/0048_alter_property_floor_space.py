# Generated by Django 3.2 on 2021-06-08 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0047_alter_deal_offer_accepted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="floor_space",
            field=models.DecimalField(
                decimal_places=2, max_digits=6, null=True
            ),
        ),
    ]
