# Generated by Django 3.2 on 2021-05-20 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0002_propertyprocess"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertyprocess",
            name="macro_status",
            field=models.CharField(
                choices=[
                    ("lettings", "Lettings"),
                    ("sales", "Sales"),
                    ("inst", "Instruction"),
                    ("view", "Viewing"),
                    ("deal", "Deal"),
                    ("comp", "Complete"),
                    ("withd", "Withdrawn"),
                ],
                max_length=40,
            ),
        ),
        migrations.AlterField(
            model_name="propertyprocess",
            name="sector",
            field=models.CharField(
                choices=[
                    ("lettings", "Lettings"),
                    ("sales", "Sales"),
                    ("inst", "Instruction"),
                    ("view", "Viewing"),
                    ("deal", "Deal"),
                    ("comp", "Complete"),
                    ("withd", "Withdrawn"),
                ],
                max_length=40,
            ),
        ),
    ]
