# Generated by Django 3.2 on 2021-05-21 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0005_instruction_instructionlettingsextra"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instruction",
            name="listing_price",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="instruction",
            name="propertyprocess",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="instruction",
                to="properties.propertyprocess",
            ),
        ),
        migrations.AlterField(
            model_name="instructionlettingsextra",
            name="propertyprocess",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="instruction_letting_extra",
                to="properties.propertyprocess",
            ),
        ),
        migrations.AlterField(
            model_name="propertyprocess",
            name="macro_status",
            field=models.CharField(
                choices=[
                    ("val", "Valuation"),
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
                choices=[("lettings", "Lettings"), ("sales", "Sales")],
                max_length=40,
            ),
        ),
    ]
