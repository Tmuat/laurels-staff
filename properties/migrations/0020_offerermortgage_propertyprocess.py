# Generated by Django 3.2 on 2021-05-26 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0019_auto_20210526_1829"),
    ]

    operations = [
        migrations.AddField(
            model_name="offerermortgage",
            name="propertyprocess",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="properties.propertyprocess",
            ),
            preserve_default=False,
        ),
    ]
