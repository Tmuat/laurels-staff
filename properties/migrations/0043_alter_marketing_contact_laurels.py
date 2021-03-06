# Generated by Django 3.2 on 2021-06-04 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0042_marketing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="marketing",
            name="contact_laurels",
            field=models.CharField(
                choices=[
                    (
                        "laurels_pro-actively_asked",
                        "Laurels Pro-actively Asked",
                    ),
                    ("social_media_message", "Social Media Message"),
                    ("phone_call_to_office", "Phone Call To Office"),
                    ("website_message", "Website Message"),
                    ("direct_email", "Direct Email"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
