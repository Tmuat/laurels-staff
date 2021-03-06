# Generated by Django 3.2 on 2021-05-26 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0013_auto_20210526_1806"),
    ]

    operations = [
        migrations.AddField(
            model_name="offerermortgage",
            name="offerer_details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offerer_mortgage_details",
                to="properties.offererdetails",
            ),
            preserve_default=False,
        ),
    ]
