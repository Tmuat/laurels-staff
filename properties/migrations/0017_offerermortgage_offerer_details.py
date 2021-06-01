# Generated by Django 3.2 on 2021-05-26 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0016_remove_offerermortgage_offerer_details"),
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