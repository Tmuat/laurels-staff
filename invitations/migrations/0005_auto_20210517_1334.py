# Generated by Django 3.2 on 2021-05-17 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invitations", "0004_alter_userinvitations_is_staff"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userinvitations",
            name="hub_targets",
        ),
        migrations.RemoveField(
            model_name="userinvitations",
            name="hub_targets_year",
        ),
        migrations.AlterField(
            model_name="userinvitations",
            name="director",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
