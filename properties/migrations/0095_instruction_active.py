# Generated by Django 3.2.4 on 2021-08-24 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0094_auto_20210819_1142"),
    ]

    operations = [
        migrations.AddField(
            model_name="instruction",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]