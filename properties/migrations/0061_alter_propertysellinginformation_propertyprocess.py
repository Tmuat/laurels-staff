# Generated by Django 3.2 on 2021-06-16 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0060_propertysellinginformation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertysellinginformation",
            name="propertyprocess",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="selling_information",
                to="properties.propertyprocess",
            ),
        ),
    ]