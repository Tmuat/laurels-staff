# Generated by Django 3.2.4 on 2021-07-23 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_rename_valuation_usertargets_valuations"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="office_comm",
        ),
    ]
