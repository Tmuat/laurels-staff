# Generated by Django 3.2.4 on 2021-07-16 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_usertargets_valuation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="usertargets",
            old_name="valuation",
            new_name="valuations",
        ),
    ]
