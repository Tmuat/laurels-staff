# Generated by Django 3.2 on 2021-05-20 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_profile_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="o_comm",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=4
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="p_comm",
            field=models.DecimalField(
                decimal_places=2, default=10, max_digits=4
            ),
        ),
    ]
