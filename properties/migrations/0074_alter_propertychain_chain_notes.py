# Generated by Django 3.2.4 on 2021-07-08 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0073_auto_20210708_1307"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertychain",
            name="chain_notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]
