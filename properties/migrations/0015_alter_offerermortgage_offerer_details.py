# Generated by Django 3.2 on 2021-05-26 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0014_offerermortgage_offerer_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offerermortgage",
            name="offerer_details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="properties.offererdetails",
            ),
        ),
    ]
