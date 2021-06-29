# Generated by Django 3.2.4 on 2021-06-25 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0065_remove_offererdetails_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="offererdetails",
            name="status",
            field=models.CharField(
                choices=[
                    ("under_offer", "Under Offer"),
                    ("no_chain", "No Chain"),
                    ("let_to_buy", "Let To Buy"),
                    ("not_on_market", "Not On Market"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]