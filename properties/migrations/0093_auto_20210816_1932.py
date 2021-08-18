# Generated by Django 3.2.4 on 2021-08-16 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0092_alter_offererdetails_completed_offer_form"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertysellinginformation",
            name="broker_phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="propertysellinginformation",
            name="buyer_phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="propertysellinginformation",
            name="buyer_sol_phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="propertysellinginformation",
            name="seller_phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="propertysellinginformation",
            name="seller_sol_phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
