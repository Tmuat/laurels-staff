# Generated by Django 3.2 on 2021-05-10 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("regionandhub", "0002_auto_20210510_0948"),
    ]

    operations = [
        migrations.AddField(
            model_name="hub",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]