# Generated by Django 3.2.4 on 2021-07-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_auto_20210715_1128"),
    ]

    operations = [
        migrations.AddField(
            model_name="usertargets",
            name="valuation",
            field=models.PositiveIntegerField(),
            preserve_default=False,
        ),
    ]
