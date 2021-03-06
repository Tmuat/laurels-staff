# Generated by Django 3.2 on 2021-06-15 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0055_delete_reductions"),
    ]

    operations = [
        migrations.AddField(
            model_name="propertyprocess",
            name="furthest_status",
            field=models.IntegerField(
                choices=[
                    (0, "Withdrawn"),
                    (1, "Awaiting Valuation"),
                    (2, "Valuation Complete"),
                    (3, "Instructed - On The Market"),
                    (4, "Deal"),
                    (5, "Complete"),
                ],
                default=1,
            ),
            preserve_default=False,
        ),
    ]
